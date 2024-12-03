from fastapi import HTTPException
from fastapi.responses import JSONResponse
from api.features.LevelUser.Services.LevelUserService import LevelUserService
from api.features.PlayerStats.Database.PlayerStatsManagementDatabaseService import PlayerStatsManagementDatabaseService
from api.services.PlayMastermindGameMVP.Configs import MastermindGameMVPConfigs
import traceback
import logging


class PlayerStatsManagementService:
    def __init__(self, PlayerDataInstance):
        self.player = PlayerDataInstance
        self.playerStatsManagementDBService = PlayerStatsManagementDatabaseService(self)
        self.levelingService = LevelUserService(self.player)

    async def setPlayerStats(self, userId: str) -> JSONResponse:
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
        try:
            await self.playerStatsManagementDBService.putPlayerStats(userId)
        except Exception as e:
            logging.error(f"Error updating player stats: {traceback.format_exc()}")
            raise HTTPException(status_code=500, detail=str(e))

        successfullyUpdatedPlayerStatsMsg = JSONResponse(
            content="Player data updated successfully.", status_code=200
        )

        return successfullyUpdatedPlayerStatsMsg

    async def assignScores(self, baseScore: int, status: str, multiplier: int, roundCount: int) -> int:
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
        return (self.__difficultyMultiplier(baseScore, difficultyMultiplier)
                + self.__roundMultiplier(baseScore, roundCounter))

    def __roundMultiplier(self, currentScore: int, currentRound: int) -> int:
        return round(currentScore * MastermindGameMVPConfigs.ROUND_MULTIPLIER[currentRound])

    def __difficultyMultiplier(self, score: int, multiplier: int) -> int:
        return round(score * multiplier)

    async def updateEndGameStats(self, gameScore: int):
        self.player.gamesPlayed += 1
        self.player.winRate = round((self.player.gamesWon / self.player.gamesPlayed) * 100)
        self.player.highestScore = max(self.player.highestScore, gameScore)
        self.levelingService.handleLeveling(gameScore)
        await self.updatePlayerStats(self.player.userId)

    async def getPlayerStatsForUserDisplay(self, userId: str) -> JSONResponse:
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
