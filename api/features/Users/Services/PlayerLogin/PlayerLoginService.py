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
        await self.playerLoginDBService.validateUserSignIn(username, password)

        await self.playerStatsService.setPlayerStats(self.player.userId)

        return JSONResponse(
            content={"message": "Player logged in successfully"},
            status_code=200
        )

    async def verifyPassword(self, plainPassword: str, hashedPassword: str) -> bool:
        return self.pwd_context.verify(plainPassword, hashedPassword)
