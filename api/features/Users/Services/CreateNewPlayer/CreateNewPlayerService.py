from fastapi import HTTPException
from fastapi.responses import JSONResponse
from api.features.Users.Database.CreateNewPlayer.CreateNewPlayerDatabaseService import CreateNewPlayerDatabaseService
from api.features.PlayerStats.Services.PlayerStatsManagementService import PlayerStatsManagementService
from passlib.context import CryptContext
import logging
import traceback

"""
Handles the creation of new player accounts, including validation, password hashing, and initializing player stats.
"""
class CreateNewPlayerService:
    def __init__(self, PlayerDataInstance):
        """
        Instantiates the player's data and auxiliary services for creating a new player.
        :param: {PlayerDataManagementService} PlayerDataInstance - Instance of player's data.
        """
        self.player = PlayerDataInstance
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self.createNewPlayerDBService = CreateNewPlayerDatabaseService(self)
        self.playerStatsService = PlayerStatsManagementService(self.player)

    async def createNewPlayer(self, username: str, password: str) -> JSONResponse:
        """
        Creates a new player with the given username and password, ensuring the username is unique and the password is
        hashed, and initializes the player's stats.
        :param: {String} username - The desired username for the new account.
        :param: {String} password - The password for the new player account.
        :return: {JSONResponse} A success message confirming account creation and providing the new userId.
        :raise: {HTTPException}
            - 400: If the username already exists in the database.
            - 500: If any error occurs during user validation, account creation, or initializing player stats.
        """
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

    def __hashPassword(self, password: str) -> str:
        """
        Hashes the user's provided password for secure storage.
        :param: {String} password - Desired password for the user's account.
        :return: {String} Securely hashed password for storing.
        """
        return self.pwd_context.hash(password)

