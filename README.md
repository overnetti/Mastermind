# Mastermind

## About

## Getting Started

## Technologies, Code Structure, and Thought Process


## API
### Endpoints

| Method | Endpoint             | Parameters                                             | Defaults | Outputs (Type and Content)                                                                                                                                                                                                                                | Purpose                                                                                                                                   |
|--------|----------------------|--------------------------------------------------------|----------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------|
| POST   | /create-user         | Users Body<br/> ```username```: String<br/> ```password```: String | N/A      | JSONResponse<br/> ```content="Account created successfully. New User Id: {userId}"```                                                                                                                                                                     | Creates both a new user in the database with a hashed password and a player instance for immediate gameplay.                              |
| POST   | /login               | Users Body<br/> ```username```: String<br/> ```password```: String | N/A      | JSONResponse<br/> ```content="Player logged in successfully."```                                                                                                                                                                                          | Logs user in and loads their player stats and data for immediate gameplay.                                                                |
| PUT    | /update-player-stats | PlayerStats Body<br/> ```userId```: String                   | N/A      | JSONResponse<br/> ```content="Player stats updated successfully."```                                                                                                                                                                                      | Updates PlayerStats table with player's new stats acquired after finishing a game.                                                        |
| POST   | /enter-game          | ModeRequest Body<br/> ```mode```: String                     | "NORMAL" | JSONResponse<br/> ```content="Player successfully entered game."```                                                                                                                                                                                       | Enters user into the game by populating the game with the corresponding configurations based on the difficulty mode (defaults to Normal). |
| POST   | /submit-guess        | GuessRequest Body<br/> ```guess```: String                   | N/A      | JSONResponse<br/> ```userId```: String,<br/> ```status```: String,<br/> ```correctNumbers```: Int,<br/> ```correctPositionsAndNumbers```: Int,<br/> ```guess```: String,<br/> ```currentRound```: Int,<br/> ```totalRounds```: Int,<br/> ```isLastRound```: Int,<br/> ```remainingGuesses```: Int | Submits a player's guess for validation and evaluation in order to generate a hint, win, or lose.                                         |
| GET    | /get-player-stats    | Query<br/> ```userId```: String                              | N/A      | JSONResponse<br/> PlayerStatsTable                                                                                                                                                                                                                        | Returns player's stats directly from the database as validation to be displayed for the user on the frontend at the end of a game.        |
| POST   | /reset               | None                                                   | N/A      | JSONResponse<br/>  ```content="Game and player have reset."```                                                                                                                                                                                            | Resets both in-memory player instance and game instance for fresh login.                                                                  |

### Sequence Diagram

## Database
### Schema
![Database Schema](assets/MastermindDatabaseSchema.svg)

## Future Implementations

### Server
- User authentication and authorization using JWT tokens, so sessions expire after a certain amount of time
- Further testing on PlayMastermindGameService and corresponding features
- Implement feature flags for each feature and dynamically adjust frontend accordingly
- Consolidate components on the frontend for more universal styles

### Features
#### LevelUserService
- Reward at specific levels
- Achievements at specific levels

## Contributions
Please feel free to contribute to this project by either submitting an issue or opening a pull request. All contributions
are welcome and encouraged :).

