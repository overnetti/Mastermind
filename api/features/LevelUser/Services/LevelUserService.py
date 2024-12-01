class LevelUserService:
    def __init__(self, PlayerDataInstance):
        self.player = PlayerDataInstance

    def handleLeveling(self, gameScore: int):
        totalXp = self.player.currentXp + gameScore

        if totalXp < self.player.xpToNextLevel:
            self.player.currentXp = totalXp
        else:
            while totalXp >= self.player.xpToNextLevel:
                totalXp -= self.player.xpToNextLevel
                self.player.currentLevel += 1
                self.player.xpToNextLevel *= 1.5

            self.player.currentXp = totalXp
