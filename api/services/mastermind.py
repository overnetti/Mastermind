from fastapi import HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.future import select
from sqlalchemy import update
from api.config import config
from api.utils import game_utils
from api.services.db import sessionLocal, UsersTable, PlayerStatsTable
from api.services.player import Player
import logging
import traceback


class Mastermind:
    def __init__(self, player: Player):
        self.player = player
        self.roundCounter = config.ROUND_COUNTER
        self.guessCount = None
        self.inputLength = None
        self.totalRounds = None
        self.remainingGuesses = None
        self.minRandomDigit = config.MIN_RAND_DIGIT
        self.maxRandomDigit = None
        self.multiplier = None
        self.baseScore = config.BASE_SCORE
        self.winningCombo = None
        self.status = None
        self.gameScore = 0

    async def enterGame(self, difficulty):
        await self.setDifficulty(difficulty)
        await self.setWinningCombo()
        return config.difficulty_modes[difficulty]

    async def setWinningCombo(self):
        self.winningCombo = game_utils.GameUtils.generateWinningCombo(
            inputLength=self.inputLength,
            minRandomDigit=self.minRandomDigit,
            maxRandomDigit=self.maxRandomDigit
        )

    async def setDifficulty(self, difficulty):
        if difficulty:
            self.guessCount = config.difficulty_modes[difficulty]["GUESS_COUNT"]
            self.inputLength = config.difficulty_modes[difficulty]["INPUT_LEN"]
            self.totalRounds = config.difficulty_modes[difficulty]["TOTAL_ROUNDS"]
            self.remainingGuesses = config.difficulty_modes[difficulty]["TOTAL_ROUNDS"]
            self.maxRandomDigit = config.difficulty_modes[difficulty]["MAX_RAND_DIGIT"]
            self.multiplier = config.difficulty_modes[difficulty]["MULTIPLIER"]
        else:
            raise ValueError('Please select a difficulty.')

    async def submitGuess(self, guess):
        if guess:  # if self.userId: Add something about must have a userId everywhere REMOVE LATER
            if not game_utils.GameUtils.isPassingRequirements(guess, self.inputLength,
                                                      self.minRandomDigit, self.maxRandomDigit):
                raise ValueError({"ERROR": "Guess does not meet requirements."})

            self.roundCounter += 1
            self.remainingGuesses -= 1
            isLastRound = self.roundCounter == self.totalRounds

            try:
                numOfMatching = game_utils.GameUtils.matchingNumbers(guess, self.winningCombo)
                numOfIndices = game_utils.GameUtils.matchingIndices(guess, self.winningCombo)

                if numOfMatching == self.inputLength and numOfIndices == self.inputLength:
                    await self.handleWin()
                elif isLastRound:
                    await self.handleGameOver()
                else:
                    self.status = "stillPlaying"

            except Exception as e:
                logging.error(f"Error with submitting guess: {traceback.format_exc()}")
                raise HTTPException(status_code=400, detail=str(e))

            return JSONResponse(content={
                "userId": self.player.userId,
                "status": self.status,
                "correctNumbers": numOfMatching,
                "correctPositions": numOfIndices,
                "currentRound": self.roundCounter,  # Remove this
                "totalRounds": self.totalRounds,  # remove this
                "isLastRound": isLastRound,
                "remainingGuesses": self.remainingGuesses,
                "winnerNumber": self.winningCombo  # REMOVE THIS
            })

    async def handleGameOver(self):
        self.gameScore = self.baseScore
        self.updateUniversalGameStats()
        await self.player.updatePlayerData(self.player.userId)
        self.resetGame()
        self.status = "lost"

    async def handleWin(self):
        self.gameScore += game_utils.GameUtils.scoring(self.baseScore, self.multiplier, self.roundCounter)
        self.player.gamesWon += 1
        self.handleLeveling(self.gameScore)
        self.updateUniversalGameStats()
        await self.player.updatePlayerData(self.player.userId)
        self.resetGame()
        self.status = "won"

    def handleLeveling(self, gameScore):
        totalXp = self.player.currentXp + gameScore

        if totalXp < self.player.xpToNextLevel:
            self.player.currentXp = totalXp
        else:
            while totalXp >= self.player.xpToNextLevel:
                totalXp -= self.player.xpToNextLevel
                self.player.currentLevel += 1
                self.player.xpToNextLevel *= 1.5

            self.player.currentXp = totalXp

    def updateUniversalGameStats(self):
        self.handleLeveling(self.gameScore)
        self.player.gamesPlayed += 1
        self.player.winRate = round((self.player.gamesWon / self.player.gamesPlayed) * 100)
        self.player.highestScore = max(self.player.highestScore, self.gameScore)

    def resetGame(self):
        self.__init__(self.player)
