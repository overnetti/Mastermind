from api.config import config
import threading
import logging
import requests


class GameUtils:
    @staticmethod
    def inputWithTimeout(prompt, timeout):
        print(prompt, end='', flush=True)
        result = [None]
        timerEvent = threading.Event()

        def getInput():
            result[0] = input()
            timerEvent.set()

        inputThread = threading.Thread(target=getInput)
        inputThread.start()
        timerEvent.wait(timeout)
        if inputThread.is_alive():
            print(f'\nGame over! You\'ve used up all of your time on this round.')
            inputThread.join()
            return None
        return result[0]

    @staticmethod
    def generateWinningCombo():
        randomdotorgResponse = requests.get("https://www.random.org/integers/",
                                            params={'num': self.inputLength, 'min': self.minRandomDigit,
                                                    'max': self.maxRandomDigit, 'col': 1, 'base': 10, 'format': 'plain',
                                                    'rnd': 'new'})
        winningValue = randomdotorgResponse.text
        joinedWinningValue = ''.join(winningValue.split())
        logging.info(f'Winning number generated: {joinedWinningValue}')
        return joinedWinningValue

    # TODO: MODIFY FOR DIFFERENT DIFFICULTIES
    @staticmethod
    def checkRequirements(userGuess):
        return len(userGuess) != self.inputLength or not userGuess.isdigit() or any(
            char in userGuess for char in ['8', '9'])

    # todo: transition self to config; or pass the winning combo to these functions probably
    @staticmethod
    def matchingNumbers(userInput):
        counter = 0
        seen = set()
        for num in str(self.winningCombo):
            if num in userInput and num not in seen:
                counter += min(userInput.count(num), str(self.winningCombo).count(num))
                seen.add(num)
        return counter

    @staticmethod
    def matchingIndices(userInput):
        counter = 0
        for i in range(len(str(self.winningCombo))):
            if str(self.winningCombo)[i] == userInput[i]:
                counter += 1
        return counter

    @staticmethod
    def roundMultiplier(currentScore, currentRound):
        return round(currentScore * config.ROUND_MULTIPLIER[currentRound])

    @staticmethod
    def scoring(currentScore, difficultyMultiplier, roundMultiplier):
        return difficultyMultiplier(currentScore) + roundMultiplier(currentScore, self.roundCounter)

