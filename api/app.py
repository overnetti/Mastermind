from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from api.services.db import initDB
from services.player import Player
from services.mastermind import Mastermind
import logging
import traceback  # REMOVE THIS LATER
import json


app = FastAPI()
player = Player()
game = Mastermind(player)

# Allows API to be queried by frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup():
    await initDB()


# User schema for FastAPI
class Users(BaseModel):
    username: str
    password: str


# Player stats schema for FastAPI
class PlayerStats(BaseModel):
    userId: str


class DifficultyRequest(BaseModel):
    difficulty: str


class GuessRequest(BaseModel):
    guess: str


@app.post("/create-user")
async def createUser(user: Users) -> str:
    try:
        response = await player.createPlayerProfile(user.username, user.password)
        return response
    except Exception as e:
        logging.error(f"Error fetching player data: {traceback.format_exc()}")
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/login")
async def login(user: Users) -> str:
    try:
        response = await player.logPlayerIn(user.username, user.password)
        return response
    except Exception as e:
        logging.error(f"Error fetching player data: {traceback.format_exc()}")
        raise HTTPException(status_code=400, detail=str(e))


@app.put("/update-player-stats")
async def updatePlayerData(stats: PlayerStats) -> str:
    try:
        response = await player.updatePlayerData(stats)
        return response
    except Exception as e:
        logging.error(f"Error fetching player data: {traceback.format_exc()}")
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/enter-game")
async def enterGame(difficulty: DifficultyRequest) -> str:
    try:
        response = await game.enterGame(difficulty.difficulty)
        return json.dumps(response)
    except Exception as e:
        logging.error(f"Error fetching player data: {traceback.format_exc()}")
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/submit-guess")
async def submitGuess(guess: GuessRequest) -> str:
    try:
        response = await game.submitGuess(guess.guess)
        return response
    except Exception as e:
        logging.error(f"Error with submitting guess: {traceback.format_exc()}")
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/get-player-stats")
async def getPlayerStats(userId: str = Query(...)) -> dict:
    try:
        response = await player.getPlayerData(userId)
        return response
    except Exception as e:
        logging.error(f"Error fetching player data: {traceback.format_exc()}")
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/reset")
async def resetGameAndPlayer() -> str:
    try:
        game.resetGame()
        player.resetPlayer()
        return "Game and player have reset."
    except Exception as e:
        logging.error(f"Error fetching player data: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=5000)
