from fastapi import HTTPException
from sqlalchemy import update
from fastapi.responses import JSONResponse
from sqlalchemy.future import select
from api.database.schema.DatabaseSchema import sessionLocal, PlayerStatsTable
import traceback
import logging


class PlayerStatsManagementDatabaseService:
    def __init__(self, PlayerStatsManagementService):
        self.playerStatsManagementService = PlayerStatsManagementService

    async def getPlayerStats(self, userId: str):
        if not userId:
            logging.error(f"Player not found: {traceback.format_exc()}")
            raise HTTPException(status_code=404, detail="Player not found. UserId is required to retrieve player stats.")

        async with sessionLocal() as session:
            result = await session.execute(select(PlayerStatsTable).where(PlayerStatsTable.userId == userId))
            return result.scalars().first()

    async def putPlayerStats(self, userId: str):
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
                        currentLevel=self.playerStatsManagementService.player.currentLevel,
                        xpToNextLevel=self.playerStatsManagementService.player.xpToNextLevel,
                        currentXp=self.playerStatsManagementService.player.currentXp,
                        highestScore=self.playerStatsManagementService.player.highestScore,
                        gamesWon=self.playerStatsManagementService.player.gamesWon,
                        gamesPlayed=self.playerStatsManagementService.player.gamesPlayed,
                        winRate=self.playerStatsManagementService.player.winRate
                    )
                )
                await session.execute(updateRequest)
                await session.commit()

            return JSONResponse(
                content="Player data updated successfully.", status_code=200
            )
