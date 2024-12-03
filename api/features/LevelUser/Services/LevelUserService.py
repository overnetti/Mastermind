import logging
import traceback
from fastapi import HTTPException


class LevelUserService:
    def __init__(self, PlayerDataInstance):
        self.player = PlayerDataInstance
        self.totalXp = None

    def handleLeveling(self, gameScore: int):
        try:
            self.totalXp = self.player.currentXp + gameScore
        except Exception as e:
            logging.error(f"Error setting totalXp in LevelUserService: {traceback.format_exc()}")
            raise HTTPException(status_code=500, detail=str(e))

        try:
            if self.totalXp < self.player.xpToNextLevel:
                self.player.currentXp = self.totalXp
            else:
                while self.totalXp >= self.player.xpToNextLevel:
                    self.totalXp -= self.player.xpToNextLevel
                    self.player.currentLevel += 1
                    self.player.xpToNextLevel *= 1.5

                self.player.currentXp = self.totalXp
        except Exception as e:
            logging.error(f"Error increasing the level of user in LevelUserService: {traceback.format_exc()}")
            raise HTTPException(status_code=500, detail=str(e))
