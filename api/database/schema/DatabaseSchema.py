from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, String, Text, Integer, Boolean
import uuid
from datetime import datetime
from fastapi import HTTPException
import traceback
import logging

databaseURL = "sqlite+aiosqlite:///./database/Mastermind.db"
engine = create_async_engine(databaseURL, echo=True)
sessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()


# Users table schema, where userId is the primary key
class UsersTable(Base):
    __tablename__ = "Users"
    userId = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    username = Column(String, unique=True, index=True)
    password = Column(String)
    createdAt = Column(String, default=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))


# PlayerStats table schema, where userId is the primary key
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

# FeatureFlag table schema, where id is the primary key
class FeatureFlag(Base):
    __tablename__="FeatureFlags"
    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    name = Column(String)
    isActive = Column(Boolean, default=0)
    createdDate = Column(String, default=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    description = Column(String)


async def initDB():
    """
    Creates the database tables if they don't already exist.
    :return: None.
    :raise: {HTTPException}:
        - 500: If an error occurs creating the database tables.
    """
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
    except Exception as e:
        logging.error(f"Error creating database tables: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=str(e))
