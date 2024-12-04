from api.database.schema.DatabaseSchema import sessionLocal, UsersTable, PlayerStatsTable
from fastapi import HTTPException
from sqlalchemy.future import select
import logging
import traceback

"""
Handles database interactions for the CreateNewPlayerService by confirming the username does not yet exist and 
storing the provided username and password in the database.
"""
class CreateNewPlayerDatabaseService:
    def __init__(self, CreateNewPlayerService):
        """
        Instantiates the CreateNewPlayerService to have access to player data.
        :param {CreateNewPlayerService} CreateNewPlayerService: An instance of the player's data from the creation service.
        """
        self.createNewPlayerService = CreateNewPlayerService

    async def validateUniqueUser(self, username: str, password: str):
        """
        Validates the user by rejecting empty params and confirming the username does not yet exist in the database.
        :param {String} username: User-provided username in attempt to create an account.
        :param {String} password: User-provided password in attempt to create an account.
        :return: None
        :raise: {HTTPException}:
            - 400: If the username or password is not provided or if the username already exists in the database.
        """
        if not username or not password:
            logging.error(f"Invalid username or password provided: {traceback.format_exc()}")
            raise HTTPException(status_code=400, detail='Not a valid username or password.')

        async with sessionLocal() as session:
            async with session.begin():

                existingUser = await session.execute(select(UsersTable).where(UsersTable.username == username))
                if existingUser.scalars().first():
                    raise HTTPException(
                        status_code=400,
                        detail='That username already exists! Please try another username or log in.'
                    )

    async def addNewUserWithStats(self, username: str, hashedPassword: str):
        """
        Makes two new entries in the database by adding a new user to the UsersTable and also adding default stats for
        them in the PlayerStatsTable.
        :param {String} username: User-provided username when creating an account.
        :param {String} hashedPassword: Hashed version of the user-provided password for creating an account.
        :return: None.
        :raise: {HTTPException}:
            - 500: If an error occurs either adding the new player to the UsersTable or PlayerStatsTable.
        """
        async with sessionLocal() as session:
            async with session.begin():
                try:
                    newUser = UsersTable(username=username, password=hashedPassword)
                    session.add(newUser)
                except Exception as e:
                    raise HTTPException(
                        status_code=500,
                        detail=f'Error adding username and password to the UsersTable: {e}'
                    )
                await session.flush()
                await session.refresh(newUser)

                self.createNewPlayerService.player.userId = newUser.userId
                self.createNewPlayerService.player.username = username

                try:
                    newPlayer = PlayerStatsTable(userId=newUser.userId)
                    session.add(newPlayer)
                except Exception as e:
                    raise HTTPException(
                        status_code=500,
                        detail=f'Error adding new user to the PlayerStatsTable: {e}'
                    )

