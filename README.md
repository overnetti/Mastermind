# Mastermind
## Dependencies
Use `install package` in root folder to download dependencies.
1. Python 3.12
2. FastAPI

# Game plan
So configs are done

questions:
1. only mastermind.py should exist
2. functions need to take the difficulty as input to determine what configs to use
5. Mastermind.py
   6. crux of the game
   7. playGame
   8. win
   9. scoring
   9. playagain? game_utils?
   10. leveling? game_utils?


# API
## Endpoints
1. make larger functions into endpoints + then assess
2. getting data on games and users for research/ensuring data persisted

### Database Schema -- SQL
Users table
1. userID
2. username
2. password

player stats
1. userId
2. currentLevel
3. xpToNextLevel
4. currentXp
5. highestScore
6. gamesWon
7. gamesPlayed
8. winRate

Multiplayer tables? How?

Must have tests for endpoints
Must have logs

Frontend stuff I have to do:
- Let user know if they have an invalid password/username combo
- Dynamically display rounds left etc. when entering game (API call returns this data)
- Dynamically display rounds left when continuing game
- Dynamically alert on frontend of insufficient values for guess 

IF I HAVE TIME:
- Pw auth