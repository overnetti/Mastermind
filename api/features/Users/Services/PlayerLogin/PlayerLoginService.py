from fastapi import HTTPException
from fastapi.responses import JSONResponse
from api.features.Users.Database.PlayerLogin.PlayerLoginDatabaseService import PlayerLoginDatabaseService
from api.features.PlayerStats.Services.PlayerStatsManagementService import PlayerStatsManagementService
from passlib.context import CryptContext
import logging
import traceback

"""
Handles logging the player into the game, including validation, password verification, and initializing player stats.
"""
class PlayerLoginService:
    def __init__(self, PlayerDataInstance):
        """
        Instantiates the player's data and auxiliary services for logging a player in.
        :param {PlayerDataManagementService} PlayerDataInstance - Instance of player's data
        """
        self.player = PlayerDataInstance
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self.playerLoginDBService = PlayerLoginDatabaseService(self)
        self.playerStatsService = PlayerStatsManagementService(self.player)

    async def logPlayerIn(self, username: str, password: str) -> JSONResponse:
        """
        Logs the player in by validating their username and password and, if validated, sets their player stats from stored data.
        :param {String} username - User-provided username in attempt to sign in.
        :param {String} password - User-provided password in attempt to sign in.
        :return: {HTTPException}:
            - 400: If an error occurs validating the user's sign in.
            - 500: If an error occurs while attempting to set the player's stats for the game.
        """
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
            content="Player logged in successfully.",
            status_code=200
        )

        return successfulLoginMsg

    async def verifyPassword(self, plainPassword: str, hashedPassword: str) -> bool:
        """
        Verifies the entered password matches the stored hashed password.
        :param {String} plainPassword - The user-provided password.
        :param {String} hashedPassword - The hashed password stored for the specific username.
        :return: {Bool} True if the passwords match, False otherwise.
        """
        return self.pwd_context.verify(plainPassword, hashedPassword)
