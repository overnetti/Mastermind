from api.config import config
from api.utils import game_utils


class Mastermind:
    def __init__(self, player):
        self.roundCounter = config.ROUND_COUNTER
        self.player = player  # todo
        self.winningCombo = game_utils.GameUtils.generateWinningCombo()

    def playGame(self):
        while True:
            if self.roundCounter == 1:
                userGuess = game_utils.GameUtils.inputWithTimeout(
                    f'Welcome to Mastermind! You are on Round {self.roundCounter} with {self.remainingGuess} remaining tries. Please guess the {self.inputLength} digit combination with numbers between {self.minRandomDigit} and {self.maxRandomDigit}. You have {self.inputTimer} seconds to guess: ',
                    self.inputTimer)
                logging.info(f'Users guess: {userGuess}')
                if not userGuess:
                    self.handleTimeout()
                    self.handlePlayAgain()
                    break
            elif self.roundCounter <= self.totalRounds and self.roundCounter != 1:
                userGuess = game_utils.GameUtils.inputWithTimeout(
                    f'You are on Round {self.roundCounter} with {self.remainingGuess} remaining tries. Please guess the {self.inputLength} digit combination with numbers between {self.minRandomDigit} and {self.maxRandomDigit}. You have {self.inputTimer} seconds to guess: ',
                    self.inputTimer)
                logging.info(f'Users guess: {userGuess}')
                if not userGuess:
                    self.handleTimeout()
                    self.handlePlayAgain()
                    break
            else:
                print('Game over! You\'ve used up all your tries.\n')
                self.player.updatePlayerData()
                self.handlePlayAgain()
                break

            if game_utils.GameUtils.checkRequirements(userGuess):
                print(f'Please input a {self.inputLength} digit number between 0 and {self.maxRandomDigit}.\n')
                logging.info(f'Please input a {self.inputLength} digit number between 0 and {self.maxRandomDigit}.\n')
                continue
            else:
                numOfMatching = game_utils.GameUtils.matchingNumbers(userGuess)
                numOfIndices = game_utils.GameUtils.matchingIndices(userGuess)

                if numOfMatching == 0 and numOfIndices == 0:
                    print('All are incorrect. Please try again.\n')
                    logging.info('Computer response: All are incorrect. Please try again.\n')
                    self.roundCounter += 1
                    self.remainingGuess -= 1
                    continue
                elif numOfMatching == self.inputLength and numOfIndices == self.inputLength:
                    self.win()
                    break
                elif numOfMatching > 0 or numOfIndices > 0:
                    print(f'{numOfMatching} correct number(s) and {numOfIndices} correct location(s).\n')
                    logging.info(
                        f'Computer response: {numOfMatching} correct number(s) and {numOfIndices} correct location(s).\n')
                    self.roundCounter += 1
                    self.remainingGuess -= 1
                    continue

    def win(self):
        self.currentScore += self.baseScore
        self.roundScore += self.scoring(self.currentScore)
        self.handleLeveling(self.roundScore)
        self.player.highestScore = max(self.player.highestScore, self.scoring(self.roundScore))
        self.player.gamesWon += 1
        self.player.winRate = round((self.player.gamesWon / self.player.gamesPlayed) * 100)
        print(f'Congratulations, you have guessed the combination! Your score is: {self.roundScore}')
        print(f'Your current XP is {self.player.currentXP}/{self.player.xpToNextLevel}\n')
        print(f'Your current win rate is: {self.player.winRate}%\n')
        logging.info(
            f'Computer response: Congratulations, you have guessed the combination! Your score is: {self.roundScore}')
        logging.info(f'Your current XP is {self.player.currentXP}/{self.player.xpToNextLevel}\n')
        logging.info(f'Your current win rate is: {self.player.winRate}%\n')
        if self.player.highestScore >= self.roundScore:
            print(f'Wow! You\'ve set a new high score: {self.player.highestScore}')
            logging.info(f'Computer response: Wow! You\'ve set a new high score: {self.player.highestScore}')
        self.player.updatePlayerData()
        self.handlePlayAgain()

    def handleTimeout(self):  # todo: maybe get rid of
        self.player.updatePlayerData()

    def handlePlayAgain(self):
        while True:
            userInput = input('Would you like to play again? (y/n): ')
            if userInput == 'y':
                self.player.gamesPlayed += 1
                self.__init__(self.player)
                self.playGame()
                break
            else:
                print('Thanks for playing!')
                break

    def handleLeveling(self, roundScore):
        if self.player.currentXP + roundScore < self.player.xpToNextLevel:
            self.player.currentXP += roundScore

        elif self.player.currentXP + roundScore >= self.player.xpToNextLevel:
            remainderXP = self.player.xpToNextLevel - self.player.currentXP
            self.player.currentXP += remainderXP
            if self.player.currentXP == self.player.xpToNextLevel:
                self.player.currentLevel += 1
                print(f'Congratulations! You are now Level {self.player.currentLevel}')
                logging.info(f'Computer response: Congratulations! You are now Level {self.player.currentLevel}')
                self.player.xpToNextLevel = self.player.xpToNextLevel * 1.5
                self.player.currentXP = 0
                self.player.currentXP = roundScore - remainderXP