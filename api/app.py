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

"""
This file contains the core API endpoints and database set up for the Mastermind game and the player's data. This file
will need to be ran in order to start the backend server.
"""

# Instantiate the FastAPI, a player instance, and an instance of the game.
app = FastAPI()
player = PlayerDataManagementService()
game = Mastermind(player)

# Ensure that the API is accessed by only the frontend.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ensure logs are not suppressed by uvicorn and are turned to debug mode.
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logging.getLogger("uvicorn").setLevel(logging.DEBUG)
logging.getLogger("uvicorn.access").setLevel(logging.DEBUG)


# Call the construction of the database tables.
@app.on_event("startup")
async def startup():
    await initDB()


# FastAPI schema for Body requests in endpoints.
class Users(BaseModel):
    username: str
    password: str


class PlayerStats(BaseModel):
    userId: str


class ModeRequest(BaseModel):
    mode: str


class GuessRequest(BaseModel):
    guess: str

# API Endpoints
@app.post("/create-user")
async def createUser(user: Users) -> JSONResponse:
    """
    Creates both a new user in the database with a hashed password and a player instance for immediate gameplay.
    :param: {Users} user: The user's username and password in the body of the request.
    :return: {JSONResponse}: Confirmation of account creation.
    :raise: {HTTPException}:
        - 400: If there is an error creating the user, perhaps due to an invalid username or password.
    """
    try:
        createNewPlayerService = CreateNewPlayerService(player)
        response = await createNewPlayerService.createNewPlayer(user.username, user.password)
        return response
    except Exception as e:
        logging.error(f"Error creating user: {traceback.format_exc()}")
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/login")
async def login(user: Users) -> JSONResponse:
    """
    Logs user in and loads their player stats and data for immediate gameplay.
    :param: {Users} user: The user's username and password in the body of the request.
    :return: {JSONResponse}: Confirmation of login.
    :raise: {HTTPException}:
        - 400: If there is an error logging in the user, perhaps due to an invalid username or password.
    """
    try:
        playerLoginService = PlayerLoginService(player)
        response = await playerLoginService.logPlayerIn(user.username, user.password)
        return response
    except Exception as e:
        logging.error(f"Error logging user into game: {traceback.format_exc()}")
        raise HTTPException(status_code=400, detail=str(e))


@app.put("/update-player-stats")
async def updatePlayerData(stats: PlayerStats) -> JSONResponse:
    """
    Updates PlayerStats table with player's new stats acquired after finishing a game.
    :param: {PlayerStats} stats: The user's userId in the body of the request.
    :return: {JSONResponse}: Confirmation of player stats update.
    :raise: {HTTPException}:
        - 400: If there is an error updating player stats, perhaps due to an invalid userId.
    """
    try:
        playerStatsService = PlayerStatsManagementService(player)
        response = await playerStatsService.updatePlayerStats(stats)
        return response
    except Exception as e:
        logging.error(f"Error updating player's stats: {traceback.format_exc()}")
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/enter-game")
async def enterGame(mode: ModeRequest) -> JSONResponse:
    """
    Enters user into the game by populating the game with the corresponding configurations based on the difficulty mode
    (defaults to Normal).
    :param: {ModeRequest} mode: The difficulty mode in the body of the request.
    :return: {JSONResponse}: Confirmation of entering the game.
    :raise: {HTTPException}:
        - 400: If there is an error entering the game, perhaps due to an invalid mode.
    """
    try:
        response = await game.enterGame(mode.mode)
        return response
    except Exception as e:
        logging.error(f"Error entering game: {traceback.format_exc()}")
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/submit-guess")
async def submitGuess(guess: GuessRequest) -> JSONResponse:
    """
    Submits a player's guess for validation and evaluation in order to generate a hint, win, or lose.
    :param: {GuessRequest} guess: The user's guess in the body of the request.
    :return: {JSONResponse}: Round data including userId, status of the game, hint data, the guess made, current round,
    total rounds, whether the user is on the last round, and remaining guesses.
    :raise: {HTTPException}:
        - 400: If there is an error submitting the guess, perhaps due to an invalid guess.
    """
    try:
        response = await game.submitGuess(guess.guess)
        if game.status == "won" or game.status == "lost":
            game.resetGame()
        return response
    except Exception as e:
        logging.error(f"Error submitting guess: {traceback.format_exc()}")
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/get-player-stats")
async def getPlayerStats(userId: str = Query(...)) -> JSONResponse:
    """
    Returns player's stats directly from the database as validation to be displayed for the user on the frontend at
    the end of a game.
    :param: {Query} userId: The user's userId in the query parameters.
    :return: {JSONResponse}: The PlayerStatsTable entry for the specific userId provided.
    :raise: {HTTPException}:
        - 400: If there is an error fetching player data, perhaps due to an invalid userId.
    """
    try:
        playerStatsService = PlayerStatsManagementService(player)
        response = await playerStatsService.getPlayerStatsForUserDisplay(userId)
        return response
    except Exception as e:
        logging.error(f"Error fetching player data: {traceback.format_exc()}")
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/reset")
async def resetGameAndPlayer() -> JSONResponse:
    """
    Resets both in-memory player instance and game instance for fresh login.
    :return: {JSONResponse}: Confirmation of game and player reset.
    :raise: {HTTPException}:
        - 500: If there is an error resetting player and game.
    """
    try:
        game.resetGame()
        player.resetPlayerData()
        return JSONResponse(content="Game and player have reset.", status_code=200)
    except Exception as e:
        logging.error(f"Error resetting player and game: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=5000, log_level="debug")
