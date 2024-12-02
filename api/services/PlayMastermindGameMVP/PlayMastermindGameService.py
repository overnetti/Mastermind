from fastapi import HTTPException
from fastapi.responses import JSONResponse
from api.clients.RandomDotOrgAPIClientRequest import RandomDotOrgAPIClientRequest
from api.features.LevelUser.Services.LevelUserService import LevelUserService
from api.features.PlayerStats.Services.PlayerStatsManagementService import PlayerStatsManagementService
from api.services.PlayMastermindGameMVP.Configs import MastermindGameMVPConfigs as Config
from api.services.PlayMastermindGameMVP.Utils import MastermindGameUtils
from api.features.PlayerData.Services.PlayerDataManagement.PlayerDataManagementService import (
    PlayerDataManagementService)
from api.features.DifficultyMode.Services.DifficultyModeService import DifficultyModeService
import logging
import traceback
import collections


class Mastermind:
    def __init__(self, player: PlayerDataManagementService):
        self.player = player
        self.levelingService = LevelUserService(self.player)
        self.playerStatsService = PlayerStatsManagementService(self.player)
        self.randomDotOrgAPIClientRequest = RandomDotOrgAPIClientRequest()
        self.difficultyModeService = DifficultyModeService(self)

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
            await self.difficultyModeService.setDifficulty(mode)
        await self.setWinningCombo()

    async def setWinningCombo(self):
        self.winningCombo = await self.randomDotOrgAPIClientRequest.generateWinningCombo(
            inputLength=self.inputLength,
            minRandomDigit=self.minRandomDigit,
            maxRandomDigit=self.maxRandomDigit
        )

    async def submitGuess(self, guess: str) -> JSONResponse:
        if self.player.userId:
            if not MastermindGameUtils.MastermindGameUtils.isPassingRequirements(guess, self.inputLength,
                                                              self.minRandomDigit, self.maxRandomDigit):
                raise ValueError({"ERROR": "Guess does not meet requirements."})

            self.__updateRoundData()

            isLastRound = self.roundCounter == self.totalRounds

            hint = self.__getHint(guess, self.winningCombo)
            numOfCorrectNums = hint["correctNumbers"]
            numOfCorrectPositionsAndNums = hint["correctPositionAndNumber"]

            try:
                hint = self.__getHint(guess, self.winningCombo)
                numOfCorrectNums = hint["correctNumbers"]
                numOfCorrectPositionsAndNums = hint["correctPositionAndNumber"]

                if numOfCorrectPositionsAndNums == self.inputLength:
                    self.player.gamesWon += 1
                    await self.handleEndGame("won")
                elif isLastRound:
                    await self.handleEndGame("lost")
                else:
                    self.status = "stillPlaying"

                # await self.__checkGameProgressStatus(numOfCorrectPositionsAndNums,
                #                                      isLastRound)

            except Exception as e:
                logging.error(f"Error submitting guess: {traceback.format_exc()}")
                raise HTTPException(status_code=400, detail=str(e))

            # TODO: Remove the winning number when ready and stop console logging
            return JSONResponse(content={
                "userId": self.player.userId,
                "status": self.status,
                "correctNumbers": str(numOfCorrectNums),
                "correctPositionsAndNumbers": str(numOfCorrectPositionsAndNums),
                "guess": guess,
                "currentRound": self.roundCounter,
                "totalRounds": self.totalRounds,
                "isLastRound": isLastRound,
                "remainingGuesses": self.remainingGuesses,
                "winnerNumber": self.winningCombo  # REMOVE THIS
            })

    def __getHint(self, guess, winningCombo) -> dict:
        correctPositionAndNumber = 0
        correctNumbers = 0

        countedNumsInWinningCombo = collections.Counter(winningCombo)
        countedNumsInGuess = collections.Counter(guess)

        for i in countedNumsInWinningCombo:
            if i in countedNumsInGuess:
                correctNumbers += min(countedNumsInWinningCombo[i], countedNumsInGuess[i])

        for i in range(len(winningCombo)):
            if winningCombo[i] == guess[i]:
                correctPositionAndNumber += 1

        return {
            "correctPositionAndNumber": correctPositionAndNumber,
            "correctNumbers": correctNumbers
        }

    def __updateRoundData(self):
        self.roundCounter += 1
        self.remainingGuesses -= 1

    # def __checkGameProgressStatus(self, numOfCorrectPositionsAndNums, isLastRound):
    #     if numOfCorrectPositionsAndNums == self.inputLength:
    #         await self.handleEndGame("won")
    #         self.player.gamesWon += 1
    #     elif isLastRound:
    #         await self.handleEndGame("lost")
    #     else:
    #         self.status = "stillPlaying"

    async def handleEndGame(self, status):
        logging.debug("this is handleEndGame")
        self.gameScore = await self.playerStatsService.assignScores(self.baseScore, status,
                                                                    self.multiplier, self.roundCounter)
        logging.debug(f"here is the gameScore: {self.gameScore}")
        await self.playerStatsService.updateEndGameStats(self.gameScore)
        self.resetGame()
        self.status = status

    def resetGame(self):
        self.__init__(self.player)
