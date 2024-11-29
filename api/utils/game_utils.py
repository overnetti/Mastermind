from api.config import config
import threading
import logging
import requests


class GameUtils:

    # todo: maybe get rid of
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
    def generateWinningCombo(inputLength, minRandomDigit, maxRandomDigit):
        randomdotorgResponse = requests.get("https://www.random.org/integers/",
                                            params={'num': inputLength, 'min': minRandomDigit,
                                                    'max': maxRandomDigit, 'col': 1, 'base': 10, 'format': 'plain',
                                                    'rnd': 'new'})
        winningValue = randomdotorgResponse.text
        joinedWinningValue = ''.join(winningValue.split())
        logging.info(f'Winning number generated: {joinedWinningValue}')
        return joinedWinningValue

    @staticmethod
    def isPassingRequirements(userGuess, inputLength, minRandomDigit, maxRandomDigit):
        return (len(userGuess) == inputLength and userGuess.isdigit and
                all(minRandomDigit <= int(char) <= maxRandomDigit for char in userGuess))

    @staticmethod
    def matchingNumbers(userInput, winningCombo):
        counter = 0
        seen = set()
        for num in str(winningCombo):
            if num in userInput and num not in seen:
                counter += min(userInput.count(num), str(winningCombo).count(num))
                seen.add(num)
        return counter

    @staticmethod
    def matchingIndices(userInput, winningCombo):
        counter = 0
        for i in range(len(str(winningCombo))):
            if str(winningCombo)[i] == userInput[i]:
                counter += 1
        return counter

    @staticmethod
    def roundMultiplier(currentScore, currentRound):
        return round(currentScore * config.ROUND_MULTIPLIER[currentRound])

    @staticmethod
    def scoring(currentScore, difficultyMultiplier, roundMultiplier, roundCounter):
        return difficultyMultiplier(currentScore) + roundMultiplier(currentScore, roundCounter)
