from api.features.DifficultyMode.Configs import DifficultyModeConfig
import logging
import traceback
from fastapi import HTTPException

"""
This service class is responsible for setting the difficulty mode of the game.
"""
class DifficultyModeService:
    def __init__(self, MastermindGameInstance):
        """
        Instantiates an instance of the game in order to manipulate the game's difficulty mode.
        :param {PlayMastermindGameService} MastermindGameInstance: Instance of the game.
        """
        self.mastermind = MastermindGameInstance

    async def setDifficulty(self, mode: str):
        """
        Depending on the mode indicated, sets the game's difficulty based on the configurations in DifficultyModeConfig.
        :param: {String} mode: The difficulty mode to set, choices are limited to the keys in DifficultyModeConfig.difficulty_modes.
        :return: None.
        :raise: {HTTPException}:
            - 404: If the mode is not found in the difficulty_modes.
            - 500: If there is an error setting the difficulty mode.
        """
        if mode:
            try:
                self.mastermind.guessCount = DifficultyModeConfig.difficulty_modes[mode]["GUESS_COUNT"]
                self.mastermind.inputLength = DifficultyModeConfig.difficulty_modes[mode]["INPUT_LEN"]
                self.mastermind.totalRounds = DifficultyModeConfig.difficulty_modes[mode]["TOTAL_ROUNDS"]
                self.mastermind.remainingGuesses = DifficultyModeConfig.difficulty_modes[mode]["TOTAL_ROUNDS"]
                self.mastermind.maxRandomDigit = DifficultyModeConfig.difficulty_modes[mode]["MAX_RAND_DIGIT"]
                self.mastermind.multiplier = DifficultyModeConfig.difficulty_modes[mode]["MULTIPLIER"]
            except Exception as e:
                logging.error(f"Error setting difficulty modes: {traceback.format_exc()}")
                raise HTTPException(status_code=500, detail=str(e))
        else:
            raise HTTPException(status_code=404, detail="Difficulty mode not found.")

