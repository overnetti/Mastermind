from fastapi import FastAPI, Path, Body, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional, List, Dict, Any, Union
from pydantic import BaseModel
from sqlalchemy import Column, String, Text, Integer
from sqlalchemy.future import select
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from datetime import datetime
import uuid
import asyncio


app = FastAPI()

# Allows API to be queried by any source
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Swap this URL with Prod DB if deploying
databaseURL = "sqlite+aiosqlite:///./database/Mastermind.db"
engine = create_async_engine(databaseURL, echo=True)
sessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()

# Users table schema
class Users(Base):
    __tablename__ = "Users"
    userId = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    username = Column(String, unique=True, index=True)
    password = Column(String)

# Player stats table schema
class PlayerStats(Base):
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


asyncio.run(initDB())

# User schema for FastAPI
class Users(BaseModel):
    userId: str
    username: str
    password: str

# Player stats schema for FastAPI
class PlayerStats(BaseModel):
    userId: str
    currentLevel: int
    xpToNextLevel: int
    currentXp: float
    highestScore: float
    gamesWon: int
    gamesPlayed: int
    winRate: float

@app.post("/create-user")
async def createUser(user: Users):
    async with sessionLocal() as session:
        async with session.begin():
            # try:
            #     userExists = await session.execute(select(Users).filter(Users.username == user.username))
            #     userExists = userExists.scalars().first()
            #     if userExists:
            #         raise HTTPException(status_code=400, detail="User already exists")
            newUser = Users(userId=user.userId, username=user.username, password=user.password)
            session.add(newUser)
            await session.commit()
            await session.refresh(newUser)
            return newUser


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=5000)
