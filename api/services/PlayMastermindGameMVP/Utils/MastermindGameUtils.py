class MastermindGameUtils:
    @staticmethod
    def isPassingRequirements(userGuess, inputLength, minRandomDigit, maxRandomDigit):
        return (len(userGuess) == inputLength and userGuess.isdigit and
                all(minRandomDigit <= int(char) <= maxRandomDigit for char in userGuess))
