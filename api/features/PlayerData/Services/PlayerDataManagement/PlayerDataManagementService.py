"""
This file contains the PlayerDataManagementService class, which is responsible for holding player data (both user info
and player stats info) in-memory.
"""
class PlayerDataManagementService:
    def __init__(self):
        """
        Initializes the PlayerDataManagementService class with both user data and player stats data.
        """
        self.username = None
        self.userId = None
        self.currentLevel = None
        self.xpToNextLevel = None
        self.currentXp = None
        self.highestScore = None
        self.gamesWon = None
        self.gamesPlayed = None
        self.winRate = None

    def resetPlayerData(self):
        """
        Resets the player's data and stats to their default values in order to end the player's session.
        :return: None.
        """
        self.__init__()


