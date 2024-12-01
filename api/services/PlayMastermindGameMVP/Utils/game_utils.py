from api.services.PlayMastermindGameMVP.Configs import MastermindGameMVPConfigs
import logging
import requests
import collections


class GameUtils:
# be in its own directory called clients and client should handle calling the api; takes in request to hit endpoint and then gives
    # back the data
    # should have error handling -- send response codes; 400, 200, 500
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
    def getHint(guess, winningCombo) -> dict:
        correctPositionAndNumber = 0
        correctNumbers = 0

        countedNumsInWinningCombo = collections.Counter(winningCombo)
        countedNumsInGuess = collections.Counter(guess)

        for i in countedNumsInWinningCombo:
            if i in countedNumsInGuess:
                correctNumbers += min(countedNumsInWinningCombo[i], countedNumsInGuess[i])

        for i in range(len(winningCombo)):
            if winningCombo[i] == guess[i]:
                correctPositionAndNumber += 1

        return {
            "correctPositionAndNumber": correctPositionAndNumber,
            "correctNumbers": correctNumbers
        }

    @staticmethod
    def roundMultiplier(currentScore, currentRound):
        return round(currentScore * MastermindGameMVPConfigs.ROUND_MULTIPLIER[currentRound])

    @staticmethod
    def difficultyMultiplier(score, multiplier):
        return round(score * multiplier)

    @staticmethod
    def scoring(currentScore, difficultyMultiplier, roundCounter):
        return (GameUtils.difficultyMultiplier(currentScore, difficultyMultiplier)
                + GameUtils.roundMultiplier(currentScore, roundCounter))
