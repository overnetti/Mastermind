class LevelUserService:
    def __init__(self, PlayerDataInstance):
        self.player = PlayerDataInstance
        self.totalXp = None

    def handleLeveling(self, gameScore: int):
        self.totalXp = self.player.currentXp + gameScore

        if self.totalXp < self.player.xpToNextLevel:
            self.player.currentXp = self.totalXp
        else:
            while self.totalXp >= self.player.xpToNextLevel:
                self.totalXp -= self.player.xpToNextLevel
                self.player.currentLevel += 1
                self.player.xpToNextLevel *= 1.5

            self.player.currentXp = self.totalXp
