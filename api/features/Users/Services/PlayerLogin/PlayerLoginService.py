from fastapi import HTTPException
from fastapi.responses import JSONResponse
from api.features.Users.Database.PlayerLogin.PlayerLoginDatabaseService import PlayerLoginDatabaseService
from api.features.PlayerStats.Services.PlayerStatsManagementService import PlayerStatsManagementService
from passlib.context import CryptContext
import logging
import traceback


class PlayerLoginService:
    def __init__(self, PlayerDataInstance):
        self.player = PlayerDataInstance
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self.playerLoginDBService = PlayerLoginDatabaseService(self)
        self.playerStatsService = PlayerStatsManagementService(self.player)

    async def logPlayerIn(self, username: str, password: str) -> JSONResponse:
        try:
            await self.playerLoginDBService.validateUserSignIn(username, password)
        except Exception as e:
            logging.error(f"Error validating user's sign in: {traceback.format_exc()}")
            raise HTTPException(status_code=400, detail=str(e))

        try:
            await self.playerStatsService.setPlayerStats(self.player.userId)
        except Exception as e:
            logging.error(f"Error setting player's stats: {traceback.format_exc()}")
            raise HTTPException(status_code=500, detail=str(e))

        successfulLoginMsg = JSONResponse(
            content={"message": "Player logged in successfully"},
            status_code=200
        )

        return successfulLoginMsg

    async def verifyPassword(self, plainPassword: str, hashedPassword: str) -> bool:
        return self.pwd_context.verify(plainPassword, hashedPassword)
