from api.services.PlayMastermindGameMVP.Configs import MastermindGameMVPConfigs


class MastermindGameUtils:

    @staticmethod
    def isPassingRequirements(userGuess, inputLength, minRandomDigit, maxRandomDigit):
        return (len(userGuess) == inputLength and userGuess.isdigit and
                all(minRandomDigit <= int(char) <= maxRandomDigit for char in userGuess))







    # todo: these might all be PlayerStats stuff
    #
    # @staticmethod
    # def roundMultiplier(currentScore, currentRound):
    #     return round(currentScore * MastermindGameMVPConfigs.ROUND_MULTIPLIER[currentRound])
    #
    # @staticmethod
    # def difficultyMultiplier(score, multiplier):
    #     return round(score * multiplier)
    #
    # @staticmethod
    # def scoring(currentScore, difficultyMultiplier, roundCounter):
    #     return (MastermindGameUtils.difficultyMultiplier(currentScore, difficultyMultiplier)
    #             + MastermindGameUtils.roundMultiplier(currentScore, roundCounter))
