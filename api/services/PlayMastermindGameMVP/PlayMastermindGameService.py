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

"""
The Mastermind class encapsulates the core logic for the Mastermind game, providing central game controller methods 
for gameplay, user input validation, scoring, game state management, and interaction with auxiliary services.
"""
class Mastermind:
    def __init__(self, player: PlayerDataManagementService):
        """
        Instantiates services and instance variables for gameplay.
        :param: {PlayerDataManagementService} player - Instance containing player's data and stats.
        """
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

    async def enterGame(self, mode="NORMAL") -> JSONResponse:
        """
        Enters the user into the game by setting the difficulty-based configurations.
        :param: {string} mode - The difficulty level of the game. Defaults to Normal.
        :return: {JSONResponse} Success message confirming player entered the game.
        :raise: {HTTPException}
            - 500: If an error occurs setting the difficulty or the winning combination.
        """
        if mode != "NORMAL":
            await self.difficultyModeService.setDifficulty(mode)
        await self.setWinningCombo()
        successfulEntryMsg = JSONResponse(
            content="Player successfully entered game.",
            status_code=200
        )
        return successfulEntryMsg

    async def setWinningCombo(self):
        """
        Sets the game instance's winning combination to the generated winning combination.
        :return: None.
        :raise: {HTTPException}:
            - 500: If an error occurs calling the Random.org API Client.
        """
        self.winningCombo = await self.randomDotOrgAPIClientRequest.generateWinningCombo(
            inputLength=self.inputLength,
            minRandomDigit=self.minRandomDigit,
            maxRandomDigit=self.maxRandomDigit
        )

    async def submitGuess(self, guess: str) -> JSONResponse:
        """
        Submits the users guess for validation and analysis while advancing the round.
        :param: {string} guess - A user's guess to be played against the winning combination.
        :return: {JSONResponse} Object containing the round's data for the frontend.
        :raise: {HTTPException}
            - 500: If an error occurs validating the guess.
            - ValueError: If the guess does not meet requirements.
        """
        try:
            guessValidation = self.__validateUserGuess(guess)
        except Exception as e:
            logging.error(f"Error validating guess: {traceback.format_exc()}")
            raise HTTPException(status_code=500, detail=str(e))

        if not guessValidation:
            raise ValueError({"ERROR": "Guess does not meet requirements."})

        self.__updateRoundData()

        isLastRound = self.roundCounter == self.totalRounds

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

        except Exception as e:
            logging.error(f"Error submitting guess: {traceback.format_exc()}")
            raise HTTPException(status_code=400, detail=str(e))

        roundData = JSONResponse(content={
            "userId": self.player.userId,
            "status": self.status,
            "correctNumbers": str(numOfCorrectNums),
            "correctPositionsAndNumbers": str(numOfCorrectPositionsAndNums),
            "guess": guess,
            "currentRound": self.roundCounter,
            "totalRounds": self.totalRounds,
            "isLastRound": isLastRound,
            "remainingGuesses": self.remainingGuesses,
        })

        return roundData

    def __getHint(self, guess: str, winningCombo: str) -> dict:
        """
        Analyzes the users guess against the winning combination to determine the count of correct numbers in the
        correct position and the count of correct numbers regardless of their position.
        :param: {String} guess - The player's current guess.
        :param: {String} winningCombo - The game's winning combination.
        :return: {Dictionary} Dict containing:
            - correctPositionAndNumber {Int} - The number of digits correctly guessed in the exact positions.
            - correctNumbers {Int} - The total count of correct digits, regardless of position.
        """
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
        """
        Updates the round data after a guess is made by incrementing the round counter and decrementing the remaining guesses.
        :return: None.
        """
        self.roundCounter += 1
        self.remainingGuesses -= 1

    def __validateUserGuess(self, guess: str) -> bool:
        """
        Validates the user's guess based on the requirements imposed by the game instance configurations.
        :param: {String} guess - User's guess.
        :return: {Boolean} True if the guess is valid, False otherwise.
        """
        if self.player.userId:
            if not MastermindGameUtils.MastermindGameUtils.isPassingRequirements(guess, self.inputLength,
                                                                                 self.minRandomDigit, self.maxRandomDigit):
                return False
            return True

    async def handleEndGame(self, status: str):
        """
        Handles end of game processes, such as assigning scores and updating player stats based on their performance.
        :param: {String} status - Final status of the game (e.g. "won" or "lost").
        :return: {HTTPException}
            - 500: If an error occurs updating the game stats.
        """
        self.status = status
        self.gameScore = await self.playerStatsService.assignScores(self.baseScore, status,
                                                                    self.multiplier, self.roundCounter)

        try:
            await self.playerStatsService.updateEndGameStats(self.gameScore)
        except Exception as e:
            logging.error(f"Error updating end game stats: {traceback.format_exc()}")
            raise HTTPException(status_code=500, detail=str(e))

    def resetGame(self):
        """
        Resets the game to its initial state for a fresh game.
        :return: None.
        :raise: {HTTPException}:
            - 400: If the player instance provided is invalid (example: user is logged out)
        """
        try:
            self.__init__(self.player)
        except Exception as e:
            logging.error(f"Error resetting the game: {traceback.format_exc()}")
            raise HTTPException(status_code=400, detail=str(e))
