from fastapi import HTTPException
from fastapi.responses import JSONResponse
from api.features.LevelUser.Services.LevelUserService import LevelUserService
from api.features.PlayerStats.Database.PlayerStatsManagementDatabaseService import PlayerStatsManagementDatabaseService
from api.services.PlayMastermindGameMVP.Configs import MastermindGameMVPConfigs
import traceback
import logging

"""
Manages the construction of and storing of player stats data at the start of and end of a game.
"""
class PlayerStatsManagementService:
    def __init__(self, PlayerDataInstance):
        """
        Instantiates the PlayerData to have access to user information, along with auxiliary services for constructing
        player stats.
        :param: {PlayerDataManagementService} PlayerDataInstance - Contains player user data such as username and userId.
        """
        self.player = PlayerDataInstance
        self.playerStatsManagementDBService = PlayerStatsManagementDatabaseService(self)
        self.levelingService = LevelUserService(self.player)

    async def setPlayerStats(self, userId: str) -> JSONResponse:
        """
        Sets the player stats in-memory for the current user at the start of a game by retrieving player stats from
        the database.
        :param: {String} userId - The userId of the current player.
        :return: {JSONResponse} - A message indicating that the player data has been set in-memory successfully.
        :raise: {HTTPException}:
            - 404: If the player stats are not found in the database.
            - 500: If an error occurs setting the player stats.
        """
        playerStats = await self.playerStatsManagementDBService.getPlayerStats(userId)

        try:
            if playerStats:
                self.player.currentLevel = playerStats.currentLevel
                self.player.xpToNextLevel = playerStats.xpToNextLevel
                self.player.currentXp = playerStats.currentXp
                self.player.highestScore = playerStats.highestScore
                self.player.gamesWon = playerStats.gamesWon
                self.player.gamesPlayed = playerStats.gamesPlayed
                self.player.winRate = playerStats.winRate
            else:
                logging.error(f"Missing player stats: {traceback.format_exc()}")
                raise HTTPException(status_code=404, detail="Player data not found.")
        except Exception as e:
            logging.error(f"Error setting player stats: {traceback.format_exc()}")
            raise HTTPException(status_code=500, detail=str(e))

        successfullySetDataMsg = JSONResponse(
            content="Player data set successfully.",
            status_code=200
        )

        return successfullySetDataMsg

    async def updatePlayerStats(self, userId: str) -> JSONResponse:
        """
        Updates the player stats in the database for the current user at the end of a game.
        :param: {String} userId - The userId of the current player.
        :return: {JSONResponse} - A message indicating that the player stats have been updated successfully.
        :raise: {HTTPException}:
            - 500: If an error occurs updating the player stats.
        """
        try:
            await self.playerStatsManagementDBService.putPlayerStats(userId)
        except Exception as e:
            logging.error(f"Error updating player stats: {traceback.format_exc()}")
            raise HTTPException(status_code=500, detail=str(e))

        successfullyUpdatedPlayerStatsMsg = JSONResponse(
            content="Player stats updated successfully.", status_code=200
        )

        return successfullyUpdatedPlayerStatsMsg

    async def assignScores(self, baseScore: int, status: str, multiplier: int, roundCount: int) -> int:
        """
        Assigns and calculates scores for the player based on whether they won or lost the game.
        :param: {Int} baseScore - The universal base score for all games set in the MastermindGameMVPConfigs.
        :param: {String} status - The status of the recently completed game, either "won" or "lost".
        :param: {Int} multiplier - The multiplier for the difficulty of the game.
        :param: {Int} roundCount - The number of rounds the player took to complete the game.
        :return: {Int} The score assigned to the player based on the game outcome and multipliers.
        :raise: {HTTPException}:
            - 500: If an error occurs calculating scores.
        """
        gameScore = 0
        try:
            if status == "lost":
                gameScore = baseScore
            elif status == "won":
                gameScore += await self.__calculateScore(baseScore, multiplier, roundCount)
            else:
                raise ValueError(f"Invalid status: {status}. Expected 'won' or 'lost'.")
        except Exception as e:
            logging.error(f"Error assigning scores: {traceback.format_exc()}")
            raise HTTPException(status_code=500, detail=str(e))

        return gameScore

    async def __calculateScore(self, baseScore: int, difficultyMultiplier: int, roundCounter: int) -> int:
        """
        Applies the difficulty multiplier and round multiplier to the base score to calculate the final score.
        :param: {Int} baseScore - The universal base score for all games set in the MastermindGameMVPConfigs.
        :param: {Int} difficultyMultiplier - The multiplier for the difficulty of the game.
        :param: {Int} roundCounter - The number of rounds the player took to complete the game in order to apply the
        correct round multiplier.
        :return: {Int} The final score calculation.
        """
        return (self.__difficultyMultiplier(baseScore, difficultyMultiplier)
                + self.__roundMultiplier(baseScore, roundCounter))

    def __roundMultiplier(self, currentScore: int, currentRound: int) -> int:
        """
        Applies the round multiplier to the score based on the round the player either won or lost on.
        :param {Int} currentScore - The current score of the player.
        :param {Int} currentRound - The round the player either won or lost on.
        :return: {Int} The score with the round multiplier applied.
        """
        return round(currentScore * MastermindGameMVPConfigs.ROUND_MULTIPLIER[currentRound])

    def __difficultyMultiplier(self, score: int, multiplier: int) -> int:
        """
        Applies the game's difficulty multiplier to the player's score.
        :param: {Int} score - The player's base score after winning or losing the game.
        :param: {Int} multiplier - The difficulty multiplier based on the difficulty of the game.
        :return: {Int} The score with the difficulty multiplier applied.
        """
        return round(score * multiplier)

    async def updateEndGameStats(self, gameScore: int):
        """
        Executes various end-of-game stat calculations for the player, such as games played, total winRate,
        highestScore, and leveling, before updating the player stats in the database.
        :param: {Int} gameScore: The player's score after receiving the multipliers.
        :return: None.
        """
        self.player.gamesPlayed += 1
        self.player.winRate = round((self.player.gamesWon / self.player.gamesPlayed) * 100)
        self.player.highestScore = max(self.player.highestScore, gameScore)
        self.levelingService.handleLeveling(gameScore)
        await self.updatePlayerStats(self.player.userId)

    async def getPlayerStatsForUserDisplay(self, userId: str) -> JSONResponse:
        """
        Retrieves the player stats from the database to display to the user at the end of a game.
        :param: {String} userId: UserId of the current player.
        :return: {JSONResponse} - The player stats for the frontend to utilize, including the userId, currentLevel,
        xpToNextLevel, currentXp, highestScore, gamesWon, gamesPlayed, and winRate.
        :raise: {HTTPException}:
            - 500: If an error occurs getting the player stats.
        """
        try:
            playerStats = await self.playerStatsManagementDBService.getPlayerStats(userId)
        except Exception as e:
            logging.error(f"Error getting player stats: {traceback.format_exc()}")
            raise HTTPException(status_code=500, detail=str(e))

        dataToDisplay = JSONResponse(
            content={
                "userId": playerStats.userId,
                "currentLevel": playerStats.currentLevel,
                "xpToNextLevel": playerStats.xpToNextLevel,
                "currentXp": playerStats.currentXp,
                "highestScore": playerStats.highestScore,
                "gamesWon": playerStats.gamesWon,
                "gamesPlayed": playerStats.gamesPlayed,
                "winRate": playerStats.winRate
            }
        )

        return dataToDisplay
