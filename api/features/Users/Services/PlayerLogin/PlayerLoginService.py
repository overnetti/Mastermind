from fastapi import HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.future import select
from api.database.schema.DatabaseSchema import sessionLocal, UsersTable
from api.features.PlayerStats.Services.PlayerStatsManagementService import PlayerStatsManagementService
from passlib.context import CryptContext
import logging
import traceback


class PlayerLoginService:
    def __init__(self, PlayerDataInstance):
        self.player = PlayerDataInstance
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self.playerStatsService = PlayerStatsManagementService(self.player)

    async def logPlayerIn(self, username: str, password: str) -> JSONResponse:
        async with sessionLocal() as session:
            async with session.begin():
                result = await session.execute(select(UsersTable).where(UsersTable.username == username))
                user = result.scalars().first()

                if not user or not await self.verifyPassword(password, user.password):
                    logging.error(f"Error validating user: {traceback.format_exc()}")
                    raise HTTPException(status_code=400, detail='Invalid username or password.')

                self.player.userId = user.userId
                self.player.username = username

                await self.playerStatsService.setPlayerStats(self.player.userId)

                return JSONResponse(
                    content={"message": "Player logged in successfully"},
                    status_code=200
                )

    async def verifyPassword(self, plainPassword: str, hashedPassword: str) -> bool:
        return self.pwd_context.verify(plainPassword, hashedPassword)
