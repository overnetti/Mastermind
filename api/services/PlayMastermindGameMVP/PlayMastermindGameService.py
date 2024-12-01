from fastapi import HTTPException
from fastapi.responses import JSONResponse
from api.features.LevelUser.Services.LevelUserService import LevelUserService
from api.features.PlayerStats.Services.PlayerStatsManagementService import PlayerStatsManagementService
from api.services.PlayMastermindGameMVP.Configs import MastermindGameMVPConfigs as Config
from api.services.PlayMastermindGameMVP.Utils import game_utils
from api.features.PlayerData.Services.PlayerDataManagement.PlayerDataManagementService import PlayerDataManagementService
from api.features.DifficultyModes.Services.SetDifficultyModeService import DifficultyModeService
import logging
import traceback


class Mastermind:
    def __init__(self, player: PlayerDataManagementService):
        self.player = player
        self.levelingService = LevelUserService(self.player)
        self.playerStatsService = PlayerStatsManagementService(self.player)

        self.roundCounter = Config.ROUND_COUNTER
        self.guessCount = Config.difficulty_modes["NORMAL"]["GUESS_COUNT"]
        self.inputLength = Config.difficulty_modes["NORMAL"]["INPUT_LEN"]
        self.totalRounds = Config.difficulty_modes["NORMAL"]["TOTAL_ROUNDS"]
        self.remainingGuesses = Config.difficulty_modes["NORMAL"]["TOTAL_ROUNDS"]
        self.minRandomDigit = Config.MIN_RAND_DIGIT
        self.maxRandomDigit = Config.difficulty_modes["NORMAL"]["MAX_RAND_DIGIT"]
        self.multiplier = Config.difficulty_modes["NORMAL"]["MULTIPLIER"]
        self.baseScore = Config.BASE_SCORE
        self.winningCombo = None
        self.status = None
        self.gameScore = 0

    async def enterGame(self, mode="NORMAL"):
        if mode != "NORMAL":
            difficultyModeService = DifficultyModeService(self)
            await difficultyModeService.setDifficulty(mode)
        await self.setWinningCombo()

    async def setWinningCombo(self):
        self.winningCombo = game_utils.GameUtils.generateWinningCombo(
            inputLength=self.inputLength,
            minRandomDigit=self.minRandomDigit,
            maxRandomDigit=self.maxRandomDigit
        )

    async def submitGuess(self, guess: str) -> JSONResponse:
        if self.player.userId:
            if not game_utils.GameUtils.isPassingRequirements(guess, self.inputLength,
                                                              self.minRandomDigit, self.maxRandomDigit):
                raise ValueError({"ERROR": "Guess does not meet requirements."})

            self.roundCounter += 1
            self.remainingGuesses -= 1
            isLastRound = self.roundCounter == self.totalRounds

            try:
                hint = game_utils.GameUtils.getHint(guess, self.winningCombo)
                numOfCorrectNums = hint["correctNumbers"]
                numOfCorrectPositionsAndNums = hint["correctPositionAndNumber"]

                if numOfCorrectPositionsAndNums == self.inputLength:
                    await self.handleWin()
                elif isLastRound:
                    await self.handleGameOver()
                else:
                    self.status = "stillPlaying"

            except Exception as e:
                logging.error(f"Error submitting guess: {traceback.format_exc()}")
                raise HTTPException(status_code=400, detail=str(e))

            # TODO: Display guess history to user using this, and stop console logging this, and remove some of this data.
            return JSONResponse(content={
                "userId": self.player.userId,
                "status": self.status,
                "correctNumbers": str(numOfCorrectNums),
                "correctPositionsAndNumbers": str(numOfCorrectPositionsAndNums),
                "currentRound": self.roundCounter,  # Remove this
                "totalRounds": self.totalRounds,  # remove this
                "isLastRound": isLastRound,
                "remainingGuesses": self.remainingGuesses,
                "winnerNumber": self.winningCombo  # REMOVE THIS
            })

    async def handleGameOver(self):
        self.gameScore = self.baseScore
        await self.playerStatsService.updateEndGameStats(self.gameScore)
        self.resetGame()
        self.status = "lost"

    async def handleWin(self):
        self.gameScore += game_utils.GameUtils.scoring(self.baseScore, self.multiplier, self.roundCounter)
        self.player.gamesWon += 1
        await self.playerStatsService.updateEndGameStats(self.gameScore)
        self.resetGame()
        self.status = "won"

    def resetGame(self):
        self.__init__(self.player)
