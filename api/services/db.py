from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, String, Text, Integer
import uuid
from datetime import datetime

databaseURL = "sqlite+aiosqlite:///./database/Mastermind.db"
engine = create_async_engine(databaseURL, echo=True)
sessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()


# Users table schema
class UsersTable(Base):
    __tablename__ = "Users"
    userId = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    username = Column(String, unique=True, index=True)
    password = Column(String)
    createdAt = Column(String, default=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))


# Player stats table schema
class PlayerStatsTable(Base):
    __tablename__="PlayerStats"
    userId = Column(String, primary_key=True, index=True)
    currentLevel = Column(Integer, default=1)
    xpToNextLevel = Column(Integer, default=100)
    currentXp = Column(Integer, default=0.0)
    highestScore = Column(Integer, default=0.0)
    gamesWon = Column(Integer, default=0)
    gamesPlayed = Column(Integer, default=0)
    winRate = Column(Integer, default=0.0)


# Creates tables if they don't already exist
async def initDB():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
