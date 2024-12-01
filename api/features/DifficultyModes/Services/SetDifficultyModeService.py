from api.features.DifficultyModes.Configs import DifficultyModesConfigs as Config


class DifficultyModeService:
    def __init__(self, MastermindGameInstance):
        self.mastermind = MastermindGameInstance

    async def setDifficulty(self, mode):
        if mode:
            self.mastermind.guessCount = Config.difficulty_modes[mode]["GUESS_COUNT"]
            self.mastermind.inputLength = Config.difficulty_modes[mode]["INPUT_LEN"]
            self.mastermind.totalRounds = Config.difficulty_modes[mode]["TOTAL_ROUNDS"]
            self.mastermind.remainingGuesses = Config.difficulty_modes[mode]["TOTAL_ROUNDS"]
            self.mastermind.maxRandomDigit = Config.difficulty_modes[mode]["MAX_RAND_DIGIT"]
            self.mastermind.multiplier = Config.difficulty_modes[mode]["MULTIPLIER"]
        else:
            raise ValueError('Please select a difficulty.')
