import logging
import traceback
from fastapi import HTTPException

"""
This service is responsible for handling the leveling of the user based on the score received at the end of a game.
"""
class LevelUserService:
    def __init__(self, PlayerDataInstance):
        """
        Instantiates the totalXp variable and PlayerDataInstance to have access to the user's data and stats.
        :param {PlayerDataManagementService} PlayerDataInstance: Contains the player's data and stats.
        """
        self.player = PlayerDataInstance
        self.totalXp = None

    def handleLeveling(self, gameScore: int):
        """
        Levels the user up by adding the score received at the end of the game to the player's totalXp,
        accounting for remainder xp to next level.
        :param: {Int} gameScore: The score the player received at the end of the game with multipliers applied.
        :return: None
        :raise: {HTTPException}:
            - 500 If an error occurs either setting the totalXp or increasing the level of the user.
        """
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
