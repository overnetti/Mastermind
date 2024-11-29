from fastapi import HTTPException
from sqlalchemy.future import select
from sqlalchemy import update
from api.config import config
from api.utils import game_utils
from api.services.db import sessionLocal, UsersTable, PlayerStatsTable
from api.services.player import Player


class Mastermind:
    def __init__(self, player: Player):
        self.player = player
        self.roundCounter = config.ROUND_COUNTER
        self.guessCount = None
        self.inputLength = None
        self.totalRounds = None
        self.remainingGuesses = None
        self.minRandomDigit = config.MIN_RAND_DIGIT
        self.maxRandomDigit = None
        self.multiplier = None
        self.baseScore = config.BASE_SCORE
        self.winningCombo = None

    async def enterGame(self, difficulty):
        await self.setDifficulty(difficulty)
        await self.setWinningCombo()
        return config.difficulty_modes[difficulty]

    async def setWinningCombo(self):
        self.winningCombo = game_utils.GameUtils.generateWinningCombo(
            inputLength=self.inputLength,
            minRandomDigit=self.minRandomDigit,
            maxRandomDigit=self.maxRandomDigit
        )

    async def setDifficulty(self, difficulty):
        if difficulty:
            self.guessCount = config.difficulty_modes[difficulty]["GUESS_COUNT"]
            self.inputLength = config.difficulty_modes[difficulty]["INPUT_LEN"]
            self.totalRounds = config.difficulty_modes[difficulty]["TOTAL_ROUNDS"]
            self.remainingGuesses = config.difficulty_modes[difficulty]["TOTAL_ROUNDS"]
            self.maxRandomDigit = config.difficulty_modes[difficulty]["MAX_RAND_DIGIT"]
            self.multiplier = config.difficulty_modes[difficulty]["MULTIPLIER"]
        else:
            raise ValueError('Please select a difficulty.')

    async def submitGuess(self, guess):
        if guess:  # if self.userId: Add something about must have a userId everywhere REMOVE LATER
            if not game_utils.GameUtils.isPassingRequirements(guess, self.inputLength,
                                                      self.minRandomDigit, self.maxRandomDigit):
                raise ValueError({"ERROR": "Guess does not meet requirements."})

            try:
                isLastRound = self.roundCounter == self.totalRounds
                numOfMatching = game_utils.GameUtils.matchingNumbers(guess, self.winningCombo)
                numOfIndices = game_utils.GameUtils.matchingIndices(guess, self.winningCombo)

                if numOfMatching == self.inputLength and numOfIndices == self.inputLength:
                    # self.win()
                    return {
                        "status": "win",
                        "correctNumbers": numOfMatching,
                        "correctPositions": numOfIndices,
                        "isLastRound": isLastRound,
                    }
                elif (numOfMatching == 0 and numOfIndices == 0) or (numOfMatching > 0 or numOfIndices > 0):
                    self.roundCounter += 1
                    self.remainingGuesses -= 1
                    return {
                        "status": "stillPlaying",
                        "correctNumbers": numOfMatching,
                        "correctPositions": numOfIndices,
                        "isLastRound": isLastRound,
                        "remainingGuesses": self.remainingGuesses
                    }

            except Exception as e:
                raise HTTPException(status_code=400, detail=str(e))

    async def handleGameOver(self):
        pass

    async def win(self):
        pass

    # def win(self):
    #     self.currentScore += self.baseScore
    #     self.roundScore += self.scoring(self.currentScore)
    #     self.handleLeveling(self.roundScore)
    #     self.player.highestScore = max(self.player.highestScore, self.scoring(self.roundScore))
    #     self.player.gamesWon += 1
    #     self.player.winRate = round((self.player.gamesWon / self.player.gamesPlayed) * 100)
    #     print(f'Congratulations, you have guessed the combination! Your score is: {self.roundScore}')
    #     print(f'Your current XP is {self.player.currentXP}/{self.player.xpToNextLevel}\n')
    #     print(f'Your current win rate is: {self.player.winRate}%\n')
    #     logging.info(
    #         f'Computer response: Congratulations, you have guessed the combination! Your score is: {self.roundScore}')
    #     logging.info(f'Your current XP is {self.player.currentXP}/{self.player.xpToNextLevel}\n')
    #     logging.info(f'Your current win rate is: {self.player.winRate}%\n')
    #     if self.player.highestScore >= self.roundScore:
    #         print(f'Wow! You\'ve set a new high score: {self.player.highestScore}')
    #         logging.info(f'Computer response: Wow! You\'ve set a new high score: {self.player.highestScore}')
    #     self.player.updatePlayerData()
    #     self.handlePlayAgain()
    #
    # def handleTimeout(self):  # todo: maybe get rid of
    #     self.player.updatePlayerData()
    #
    # def handlePlayAgain(self):
    #     while True:
    #         userInput = input('Would you like to play again? (y/n): ')
    #         if userInput == 'y':
    #             self.player.gamesPlayed += 1
    #             self.__init__(self.player)
    #             self.playGame()
    #             break
    #         else:
    #             print('Thanks for playing!')
    #             break
    #
    # def handleLeveling(self, roundScore):
    #     if self.player.currentXP + roundScore < self.player.xpToNextLevel:
    #         self.player.currentXP += roundScore
    #
    #     elif self.player.currentXP + roundScore >= self.player.xpToNextLevel:
    #         remainderXP = self.player.xpToNextLevel - self.player.currentXP
    #         self.player.currentXP += remainderXP
    #         if self.player.currentXP == self.player.xpToNextLevel:
    #             self.player.currentLevel += 1
    #             print(f'Congratulations! You are now Level {self.player.currentLevel}')
    #             logging.info(f'Computer response: Congratulations! You are now Level {self.player.currentLevel}')
    #             self.player.xpToNextLevel = self.player.xpToNextLevel * 1.5
    #             self.player.currentXP = 0
    #             self.player.currentXP = roundScore - remainderXP