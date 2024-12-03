from api.database.schema.DatabaseSchema import sessionLocal, UsersTable, PlayerStatsTable
from fastapi import HTTPException
from sqlalchemy.future import select
import logging
import traceback


class CreateNewPlayerDatabaseService:
    def __init__(self, CreateNewPlayerService):
        self.createNewPlayerService = CreateNewPlayerService

    async def validateUniqueUser(self, username: str, password: str):
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
        async with sessionLocal() as session:
            async with session.begin():
                newUser = UsersTable(username=username, password=hashedPassword)
                session.add(newUser)
                await session.flush()
                await session.refresh(newUser)

                self.createNewPlayerService.player.userId = newUser.userId
                self.createNewPlayerService.player.username = username

                newPlayer = PlayerStatsTable(userId=newUser.userId)
                session.add(newPlayer)

