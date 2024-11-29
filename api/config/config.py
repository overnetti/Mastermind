# Game configurations
ROUND_COUNTER = 1
CURRENT_SCORE = 0
ROUND_SCORE = 0
MIN_RAND_DIGIT = 0
INPUT_TIMER = 30
TOTAL_ROUNDS = 10
BASE_SCORE = 100
ROUND_MULTIPLIER = {
    1: 2,
    2: 1.9,
    3: 1.8,
    4: 1.7,
    5: 1.6,
    6: 1.5,
    7: 1.4,
    8: 1.3,
    9: 1.2,
    10: 1.1
}

# Difficulty configs
difficulty_modes = {
    "EASY": {
        "GUESS_COUNT": 10,
        "INPUT_LEN": 4,
        "TOTAL_ROUNDS": 10,
        "MAX_RAND_DIGIT": 5,
        "MULTIPLIER": 0.5
    },
    "NORMAL": {
        "GUESS_COUNT": 10,
        "INPUT_LEN": 4,
        "TOTAL_ROUNDS": 10,
        "MAX_RAND_DIGIT": 7,
        "MULTIPLIER": 1
    },
    "HARD": {
        "GUESS_COUNT": 10,
        "INPUT_LEN": 6,
        "TOTAL_ROUNDS": 10,
        "MAX_RAND_DIGIT": 9,
        "MULTIPLIER": 2
    },
    "IMPOSSIBLE": {
        "GUESS_COUNT": 5,
        "INPUT_LEN": 10,
        "TOTAL_ROUNDS": 5,
        "MAX_RAND_DIGIT": 9,
        "MULTIPLIER": 4
    }
}
