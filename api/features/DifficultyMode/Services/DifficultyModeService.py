from api.features.DifficultyMode.Configs import DifficultyModeConfig


class DifficultyModeService:
    def __init__(self, MastermindGameInstance):
        self.mastermind = MastermindGameInstance

    async def setDifficulty(self, mode):
        if mode:
            self.mastermind.guessCount = DifficultyModeConfig.difficulty_modes[mode]["GUESS_COUNT"]
            self.mastermind.inputLength = DifficultyModeConfig.difficulty_modes[mode]["INPUT_LEN"]
            self.mastermind.totalRounds = DifficultyModeConfig.difficulty_modes[mode]["TOTAL_ROUNDS"]
            self.mastermind.remainingGuesses = DifficultyModeConfig.difficulty_modes[mode]["TOTAL_ROUNDS"]
            self.mastermind.maxRandomDigit = DifficultyModeConfig.difficulty_modes[mode]["MAX_RAND_DIGIT"]
            self.mastermind.multiplier = DifficultyModeConfig.difficulty_modes[mode]["MULTIPLIER"]
        else:
            raise ValueError('Please select a difficulty.')
