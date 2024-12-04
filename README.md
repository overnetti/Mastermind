# Mastermind
Welcome to Mastermind, a code-breaking game where players guess the correct sequence of numbers within a set number of attempts!

## About
Mastermind is a logic-based game designed to challenge your deductive reasoning skills. Players attempt to uncover a hidden code by making guesses and receiving hints about the accuracy of their numbers and positions.

This is a full-stack version of the game that utilizes a React frontend, a FastAPI backend, and a SQL database.

### Additional features
The game also includes the following additional features:
- Choice of Difficulty Modes: Easy, Normal, Hard, and Impossible
  - Easy: 4 digits ranging from 0 to 5, 10 guesses
  - Normal: 4 digits ranging from 0 to 7, 10 guesses (core game)
  - Hard: 6 digits between 0 and 9, 10 guesses
  - Impossible: 10 digits between 0 and 9, 5 guesses
- Account creation and login
- Leveling System: Players level up quickest by winning games but receive some XP for trying as well
- Player Statistics which track a user's:
  - Current level
  - Experience needed to attain the next level
  - Current amount of experience
  - Highest score ever achieved
  - Total number of games won
  - Total number of games played
  - Win rate

## Getting Started
Before beginning, make sure you have [NodeJS](https://nodejs.org/en) and [Python3.12](https://www.python.org/downloads/release/python-3120/) installed.

1. Clone the repository
   - Clone the following repo to your machine:
`git clone https://github.com/overnetti/Mastermind.git`
2. Install dependencies:
   - Navigate to the root directory of the project
   - For the frontend, change directories to the `mastermind-frontend` folder:
     - `cd mastermind-frontend`
   - And run:
     - `npm install`
   - For the backend, change directories to the `api` folder:
     - `cd ../api` 
   - And run:
     - `pip install -r requirements.txt`
   - For the database, ensure you have a SQL database viewer on your machine (e.g. [DBeaver](https://dbeaver.io/download/), [MySQL Workbench](https://dev.mysql.com/downloads/workbench/), [DB Browser for SQL Lite](https://sqlitebrowser.org/dl/), etc.)

### Running the Application
#### Frontend (port 3000)
   - Navigate to the `mastermind-frontend` folder:
     - `cd mastermind-frontend`
   - Run the following command:
     - `npm start`

#### Backend (port 5000)
   - Navigate to the root directory of the project and run:
     - `python3.12 -m api.app`

## API
This API runs on FastAPI. Documentation on FastAPI can be found [here](https://devdocs.io/fastapi/).

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
[Insert sequence diagram]

## Database
### Schema
![Database Schema](assets/MastermindDatabaseSchema.svg)

## Technologies, Code Structure, and Thought Process
### Technologies with Documentation
- [NodeJS](https://nodejs.org/api/index.html)
- [React](https://react.dev/learn)
- [FastAPI](https://devdocs.io/fastapi/)
- [SQLite](https://www.sqlite.org/quickstart.html)
- [SQLAlchemy](https://docs.sqlalchemy.org/en/20/tutorial/index.html)
- [AioSQLite](https://aiosqlite.omnilib.dev/en/stable/) 
- [Requests](https://requests.readthedocs.io/en/latest/)
- [Pydantic](https://docs.pydantic.dev/latest/)
- [greenlet](https://greenlet.readthedocs.io/en/latest/)
- [Passlib](https://passlib.readthedocs.io)
- [Bcrypt](https://www.geeksforgeeks.org/hashing-passwords-in-python-with-bcrypt/)

### Code Structure

### Thought Process

## Future Implementations
### Server
- Implement controllers to call business and DB logic functions within endpoints
- User authentication and authorization using JWT tokens, so sessions expire after a certain amount of time
- Further testing on PlayMastermindGameService and corresponding features
- Implement feature flags for each feature and dynamically adjust frontend accordingly
- Consolidate components on the frontend for more universal styles

### Features
#### LevelUserService
- Reward at specific levels
- Achievements at specific levels

#### Users
- More data collection when creating a user
- Tracking sessionIds for a game session

## Contributions
Please feel free to contribute to this project by either submitting an issue or opening a pull request. All contributions
are welcome and encouraged :).

