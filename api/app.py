from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from api.services.db import initDB
from services.player import Player


app = FastAPI()

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
    # currentLevel: int
    # xpToNextLevel: int
    # currentXp: float
    # highestScore: float
    # gamesWon: int
    # gamesPlayed: int
    # winRate: float


@app.post("/create-user")
async def createUser(user: Users) -> str:
    try:
        player = Player(username=user.username, password=user.password)
        response = await player.createPlayerProfile(user.username, user.password)
        return response
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/login")
async def login(user: Users) -> str:
    try:
        player = Player(username=user.username, password=user.password)
        response = await player.logPlayerIn(user.username, user.password)
        return response
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.put("/update-player-stats")
async def updatePlayerData(stats: PlayerStats) -> str:
    try:
        player = Player()
        response = await player.updatePlayerData(stats)
        return response
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=5000)
