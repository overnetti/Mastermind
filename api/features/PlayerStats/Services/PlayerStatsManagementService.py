from fastapi import HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.future import select
from sqlalchemy import update
from api.database.schema.DatabaseSchema import sessionLocal, PlayerStatsTable
from api.features.LevelUser.Services.LevelUserService import LevelUserService
from api.services.PlayMastermindGameMVP.Configs import MastermindGameMVPConfigs
import traceback
import logging


class PlayerStatsManagementService:
    def __init__(self, PlayerDataInstance):
        self.player = PlayerDataInstance
        self.levelingService = LevelUserService(self.player)

    async def setPlayerStats(self, userId: str) -> JSONResponse:
        async with sessionLocal() as session:
            result = await session.execute(select(PlayerStatsTable).where(PlayerStatsTable.userId == userId))
            playerStats = result.scalars().first()

            if playerStats:
                self.player.currentLevel = playerStats.currentLevel
                self.player.xpToNextLevel = playerStats.xpToNextLevel
                self.player.currentXp = playerStats.currentXp
                self.player.highestScore = playerStats.highestScore
                self.player.gamesWon = playerStats.gamesWon
                self.player.gamesPlayed = playerStats.gamesPlayed
                self.player.winRate = playerStats.winRate
            else:
                logging.error(f"Error with setting player stats: {traceback.format_exc()}")
                raise HTTPException(status_code=404, detail="Player data not found.")

            return JSONResponse(
                content="Player data set successfully.",
                status_code=200
            )

    async def updatePlayerStats(self, userId: str) -> JSONResponse:
        if not userId:
            logging.error(f"Error with updating player stats: {traceback.format_exc()}")
            raise HTTPException(status_code=400, detail='UserId required to update player data.')

        async with sessionLocal() as session:
            async with session.begin():
                result = await session.execute(select(PlayerStatsTable).where(PlayerStatsTable.userId == userId))
                playerStats = result.scalars().first()

                if not playerStats:
                    logging.error(f"Player stats missing: {traceback.format_exc()}")
                    raise HTTPException(status_code=404, detail="Player stats not found.")

                updateRequest = (
                    update(PlayerStatsTable)
                    .where(PlayerStatsTable.userId == userId).values(
                        currentLevel=self.player.currentLevel,
                        xpToNextLevel=self.player.xpToNextLevel,
                        currentXp=self.player.currentXp,
                        highestScore=self.player.highestScore,
                        gamesWon=self.player.gamesWon,
                        gamesPlayed=self.player.gamesPlayed,
                        winRate=self.player.winRate
                    )
                )
                await session.execute(updateRequest)
                await session.commit()

            return JSONResponse(
                content="Player data updated successfully.", status_code=200
            )

    async def assignScores(self, baseScore, status, multiplier, roundCount):
        gameScore = 0

        if status == "lost":
            gameScore = baseScore

        elif status == "won":
            gameScore += await self.__calculateScore(baseScore, multiplier, roundCount)

        else:
            raise ValueError(f"Invalid status: {status}. Expected 'won' or 'lost'.")

        return gameScore

    async def __calculateScore(self, baseScore, difficultyMultiplier, roundCounter):
        return (self.__difficultyMultiplier(baseScore, difficultyMultiplier)
                + self.__roundMultiplier(baseScore, roundCounter))

    def __roundMultiplier(self, currentScore, currentRound):
        return round(currentScore * MastermindGameMVPConfigs.ROUND_MULTIPLIER[currentRound])

    def __difficultyMultiplier(self, score, multiplier):
        return round(score * multiplier)

    async def updateEndGameStats(self, gameScore: int):
        self.player.gamesPlayed += 1
        self.player.winRate = round((self.player.gamesWon / self.player.gamesPlayed) * 100)
        self.player.highestScore = max(self.player.highestScore, gameScore)
        self.levelingService.handleLeveling(gameScore)
        await self.updatePlayerStats(self.player.userId)

    async def getPlayerStats(self, userId: str) -> JSONResponse:
        if not userId:
            logging.error(f"Player not found: {traceback.format_exc()}")
            raise HTTPException(status_code=404, detail="Player not found. UserId is required to retrieve player stats.")

        async with sessionLocal() as session:
            async with session.begin():
                result = await session.execute(select(PlayerStatsTable).where(PlayerStatsTable.userId == userId))
                playerStats = result.scalars().first()

                if not playerStats:
                    logging.error(f"Player stats not found: {traceback.format_exc()}")
                    raise HTTPException(status_code=404, detail="Player stats were not found.")

                return JSONResponse(
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
