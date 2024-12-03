from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from api.database.schema.DatabaseSchema import initDB
from api.features.Users.Services.CreateNewPlayer.CreateNewPlayerService import CreateNewPlayerService
from api.features.PlayerData.Services.PlayerDataManagement.PlayerDataManagementService import (
    PlayerDataManagementService)
from api.features.Users.Services.PlayerLogin.PlayerLoginService import PlayerLoginService
from api.features.PlayerStats.Services.PlayerStatsManagementService import PlayerStatsManagementService
from api.services.PlayMastermindGameMVP.PlayMastermindGameService import Mastermind
import logging
import traceback
import json


app = FastAPI()
player = PlayerDataManagementService()
game = Mastermind(player)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger("uvicorn")

logging.getLogger("uvicorn").setLevel(logging.DEBUG)
logging.getLogger("uvicorn.access").setLevel(logging.DEBUG)


@app.on_event("startup")
async def startup():
    await initDB()


class Users(BaseModel):
    username: str
    password: str


class PlayerStats(BaseModel):
    userId: str


class ModeRequest(BaseModel):
    mode: str


class GuessRequest(BaseModel):
    guess: str


@app.post("/create-user")
async def createUser(user: Users) -> JSONResponse:
    try:
        createNewPlayerService = CreateNewPlayerService(player)
        response = await createNewPlayerService.createNewPlayer(user.username, user.password)
        return response
    except Exception as e:
        logging.error(f"Error fetching player data: {traceback.format_exc()}")
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/login")
async def login(user: Users) -> JSONResponse:
    try:
        playerLoginService = PlayerLoginService(player)
        response = await playerLoginService.logPlayerIn(user.username, user.password)
        return response
    except Exception as e:
        logging.error(f"Error fetching player data: {traceback.format_exc()}")
        raise HTTPException(status_code=400, detail=str(e))


@app.put("/update-player-stats")
async def updatePlayerData(stats: PlayerStats) -> JSONResponse:
    try:
        playerStatsService = PlayerStatsManagementService(player)
        response = await playerStatsService.updatePlayerStats(stats)
        return response
    except Exception as e:
        logging.error(f"Error fetching player data: {traceback.format_exc()}")
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/enter-game")
async def enterGame(mode: ModeRequest) -> str:
    try:
        response = await game.enterGame(mode.mode)
        return json.dumps(response)
    except Exception as e:
        logging.error(f"Error fetching player data: {traceback.format_exc()}")
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/submit-guess")
async def submitGuess(guess: GuessRequest) -> JSONResponse:
    try:
        response = await game.submitGuess(guess.guess)
        if game.status == "won" or game.status == "lost":
            game.resetGame()
        return response
    except Exception as e:
        logging.error(f"Error with submitting guess: {traceback.format_exc()}")
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/get-player-stats")
async def getPlayerStats(userId: str = Query(...)) -> JSONResponse:
    try:
        playerStatsService = PlayerStatsManagementService(player)
        response = await playerStatsService.getPlayerStatsForUserDisplay(userId)
        return response
    except Exception as e:
        logging.error(f"Error fetching player data: {traceback.format_exc()}")
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/reset")
async def resetGameAndPlayer() -> str:
    try:
        game.resetGame()
        player.resetPlayerData()
        return "Game and player have reset."
    except Exception as e:
        logging.error(f"Error fetching player data: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=5000, log_level="debug")
