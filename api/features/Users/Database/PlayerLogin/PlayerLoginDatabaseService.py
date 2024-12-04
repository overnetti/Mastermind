from fastapi import HTTPException
from sqlalchemy.future import select
from api.database.schema.DatabaseSchema import sessionLocal, UsersTable
import logging
import traceback

"""
Handles database interactions for the PlayerLoginService by verifying the provided username and password exists and matches
the records in the database.
"""
class PlayerLoginDatabaseService:
    def __init__(self, PlayerLoginService):
        """
        Instantiates the login service to have access to player data.
        :param {PlayerLoginService} PlayerLoginService - An instance of the player's data from the login service.
        """
        self.playerLoginService = PlayerLoginService

    async def validateUserSignIn(self, username: str, password: str):
        """
        Validates the user's attempt to sign in by looking for the indicated username in the database and comparing the
        provided password with the hashed password for that specific username.
        :param {String} username - User-provided username in an attempt to sign in.
        :param {String} password - User-provided password in an attempt to sign in.
        :return: None.
        :raise: {HTTPException}:
            - 400: If an error occurs finding the user or verifying the password.
        """
        async with sessionLocal() as session:
            async with session.begin():
                result = await session.execute(select(UsersTable).where(UsersTable.username == username))
                user = result.scalars().first()

                if not user or not await self.playerLoginService.verifyPassword(password, user.password):
                    logging.error(f"Error validating user: {traceback.format_exc()}")
                    raise HTTPException(status_code=400, detail='Invalid username or password.')

                self.playerLoginService.player.userId = user.userId
                self.playerLoginService.player.username = username
