from api.features.DifficultyMode.Configs import DifficultyModeConfig
import logging
import traceback
from fastapi import HTTPException


class DifficultyModeService:
    def __init__(self, MastermindGameInstance):
        self.mastermind = MastermindGameInstance

    async def setDifficulty(self, mode: str):
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
            raise ValueError('Please select a difficulty.')
