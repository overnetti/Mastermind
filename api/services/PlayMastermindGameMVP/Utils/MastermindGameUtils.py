"""
Utility class for Mastermind game-related helper functions.
"""
class MastermindGameUtils:
    @staticmethod
    def isPassingRequirements(userGuess: str, inputLength: int, minRandomDigit: int, maxRandomDigit: int) -> bool:
        """
        Validates if the user's guess meets the game's requirements based on the configurations.
        @param {String} userGuess - The user's guess.
        @param {Int} inputLength - Required length of the guess.
        @param {Int} minRandomDigit - Minimum valid digit in the guess.
        @param {Int} maxRandomDigit - Maximum valid digit in the guess.
        @returns {bool} True if guess meets the criteria, False otherwise.
        """
        return (len(userGuess) == inputLength and userGuess.isdigit and
                all(minRandomDigit <= int(char) <= maxRandomDigit for char in userGuess))
