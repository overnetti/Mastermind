from fastapi import HTTPException
from fastapi.responses import JSONResponse
from api.features.Users.Database.CreateNewPlayer.CreateNewPlayerDatabaseService import CreateNewPlayerDatabaseService
from api.features.PlayerStats.Services.PlayerStatsManagementService import PlayerStatsManagementService
from passlib.context import CryptContext
import logging
import traceback


class CreateNewPlayerService:
    def __init__(self, PlayerDataInstance):
        self.player = PlayerDataInstance
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self.createNewPlayerDBService = CreateNewPlayerDatabaseService(self)
        self.playerStatsService = PlayerStatsManagementService(self.player)

    async def createNewPlayer(self, username: str, password: str) -> JSONResponse:
        try:
            existingUser = await self.createNewPlayerDBService.validateUniqueUser(username, password)
        except Exception as e:
            logging.error(f"Error checking for existing users: {traceback.format_exc()}")
            raise HTTPException(status_code=500, detail=str(e))

        if existingUser:
            raise HTTPException(
                status_code=400,
                detail='That username already exists! Please try another username or log in.'
            )

        hashedPassword = self.__hashPassword(password)

        try:
            await self.createNewPlayerDBService.addNewUserWithStats(username, hashedPassword)
        except Exception as e:
            logging.error(f"Error adding new user and stats: {traceback.format_exc()}")
            raise HTTPException(status_code=500, detail=str(e))


        try:
            await self.playerStatsService.setPlayerStats(self.player.userId)
        except Exception as e:
            logging.error(f"Error setting player stats: {traceback.format_exc()}")
            raise HTTPException(status_code=500, detail=str(e))

        return JSONResponse(
            content="Account created successfully. New UserId: " + self.player.userId,
            status_code=200
        )

    def __hashPassword(self, password):
        return self.pwd_context.hash(password)

