from fastapi import HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.future import select
from api.database.schema.DatabaseSchema import sessionLocal, UsersTable, PlayerStatsTable
from api.features.PlayerStats.Services.PlayerStatsManagementService import PlayerStatsManagementService
from passlib.context import CryptContext
import logging
import traceback


class CreateNewPlayerService:
    def __init__(self, PlayerDataInstance):
        self.player = PlayerDataInstance
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self.playerStatsService = PlayerStatsManagementService(self.player)

    async def createNewPlayer(self, username: str, password: str) -> JSONResponse:

        # todo: one single validate (20 thro 32)
        if not username or not password:
            logging.error(f"Invalid username or password provided: {traceback.format_exc()}")
            raise HTTPException(status_code=400, detail='Not a valid username or password.')

        # todo: Db file, get func
        async with sessionLocal() as session:
            async with session.begin():

                existingUser = await session.execute(select(UsersTable).where(UsersTable.username == username))
                if existingUser.scalars().first():
                    raise HTTPException(
                        status_code=400,
                        detail='That username already exists! Please try another username or log in.'
                    )

                # todo: add another priv method hashPassword
                hashedPassword = self.pwd_context.hash(password)

                # todo: all these interactions is a set func in DB file
                newUser = UsersTable(username=username, password=hashedPassword)
                session.add(newUser)
                await session.flush()
                await session.refresh(newUser)

                self.player.userId = newUser.userId
                self.player.username = username

                # todo: set the playerstats, this can live in DB file for player stats
                newPlayer = PlayerStatsTable(userId=newUser.userId)
                session.add(newPlayer)

        await self.playerStatsService.setPlayerStats(self.player.userId)

        return JSONResponse(
            content="Account created successfully. New UserId: " + newUser.userId,
            status_code=200
        )