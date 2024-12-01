class PlayerDataManagementService:
    def __init__(self):
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
        self.__init__()


