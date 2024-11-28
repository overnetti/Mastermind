from fastapi import HTTPException
from sqlalchemy.future import select
from sqlalchemy import update
from api.services.db import sessionLocal, UsersTable, PlayerStatsTable
from passlib.context import CryptContext


class Player:
    def __init__(self, username: str = None, password: str = None):
        self.username = username
        self.password = password
        self.userId = None
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self.currentLevel = None
        self.xpToNextLevel = None
        self.currentXp = None
        self.highestScore = None
        self.gamesWon = None
        self.gamesPlayed = None
        self.winRate = None

    async def createPlayerProfile(self, username: str, password: str) -> str:
        if not username or not password:
            raise HTTPException(status_code=400, detail='Not a valid username or password.')

        hashedPassword = self.pwd_context.hash(password)

        async with sessionLocal() as session:
            async with session.begin():

                existingUser = await session.execute(select(UsersTable).where(UsersTable.username == username))
                if existingUser.scalars().first():
                    raise HTTPException(
                        status_code=400,
                        detail='That username already exists! Please try another username or log in.'
                    )

                newUser = UsersTable(username=username, password=hashedPassword)
                session.add(newUser)
                await session.flush()
                await session.refresh(newUser)

                self.userId = newUser.userId

                newPlayer = PlayerStatsTable(userId=newUser.userId)
                session.add(newPlayer)

                await self.setPlayerData(self.userId)

        return "Account created successfully. New UserId: " + newUser.userId

    async def logPlayerIn(self, username: str, password: str) -> str:
        async with sessionLocal() as session:
            async with session.begin():
                result = await session.execute(select(UsersTable).where(UsersTable.username == username))
                user = result.scalars().first()

                if not user or not await self.verifyPassword(password, user.password):
                    raise HTTPException(status_code=400, detail='Invalid username or password.')

                self.userId = user.userId

                await self.setPlayerData(self.userId)

                return "Login successful."

    async def verifyPassword(self, plainPassword: str, hashedPassword: str) -> bool:
        return self.pwd_context.verify(plainPassword, hashedPassword)

    async def setPlayerData(self, userId: str):
        async with sessionLocal() as session:
            result = await session.execute(select(PlayerStatsTable).where(PlayerStatsTable.userId == userId))
            playerStats = result.scalars().first()

            if playerStats:
                self.currentLevel = playerStats.currentLevel
                self.xpToNextLevel = playerStats.xpToNextLevel
                self.currentXp = playerStats.currentXp
                self.highestScore = playerStats.highestScore
                self.gamesWon = playerStats.gamesWon
                self.gamesPlayed = playerStats.gamesPlayed
                self.winRate = playerStats.winRate
            else:
                raise HTTPException(status_code=404, detail="Player data not found.")

    async def updatePlayerData(self, userId):
        if not userId:
            raise HTTPException(status_code=400, detail='UserId required to update player data.')

        async with sessionLocal() as session:
            async with session.begin():
                result = await session.execute(select(PlayerStatsTable).where(PlayerStatsTable.userId == userId))
                playerStats = result.scalars().first()

                if not playerStats:
                    raise HTTPException(status_code=404, detail="Player data not found.")

                updateRequest = (
                    update(PlayerStatsTable)
                    .where(PlayerStatsTable.userId == userId).values(
                        currentLevel=self.currentLevel,
                        xpToNextLevel=self.xpToNextLevel,
                        currentXp=self.currentXp,
                        highestScore=self.highestScore,
                        gamesWon=self.gamesWon,
                        gamesPlayed=self.gamesPlayed,
                        winRate=self.winRate
                    )
                )
                await session.execute(updateRequest)
                await session.commit()

            return "Player data updated successfully."

