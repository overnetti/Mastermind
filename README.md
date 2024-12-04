# Mastermind
Welcome to Mastermind, a code-breaking game where players guess the correct sequence of numbers within a set number of attempts!

## About
Mastermind is a logic-based game designed to challenge your deductive reasoning skills. Players attempt to uncover a hidden code by making guesses and receiving hints about the accuracy of their numbers and positions.

This is a full-stack version of the game that utilizes a React frontend, a FastAPI backend, and a SQLite database.

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
Before beginning, ensure you have [NodeJS](https://nodejs.org/en) and [Python3.12](https://www.python.org/downloads/release/python-3120/) installed.

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
   - Navigate to the `mastermind-frontend` folder from the root directory:
     - `cd mastermind-frontend`
   - Run the following command:
     - `npm start`

#### Backend (port 5000)
   - Navigate to the root directory of the project and run:
     - `python3.12 -m api.app`

### Testing
Currently, only the backend is tested. Both GetHintTests and SubmitGuessTests live in the `./services/PlayMastermindGameMVP/Tests` directory.

From the root directory, run:
- for GetHintTests: ```python3.12 -m unittest api.services.PlayMastermindGameMVP.Tests.GetHintTests```
- for SubmitGuessTests: ```python3.12 -m unittest api.services.PlayMastermindGameMVP.Tests.SubmitGuessTests```

### Playing the Game
1. Open your web browser and navigate to http://localhost:3000/ to start playing the game.
   - Ensure port 3000 is not already in use.
2. If you're a returning player, select Returning Player. Otherwise, select Create New User.
   - If returning player:
      - Enter your username and password to sign in.
   - If new user:
      - Enter your desired username and password. Your password must be over 8 characters long.
3. Select a difficulty mode for the game.
4. Make a guess by clicking the Guess button. Your guess history will show up as you make guesses.
5. Whether you win or lose, you'll be presented your stats and an option to Play Again or Logout.

Happy Masterminding!

## API
This API runs on FastAPI. Documentation on FastAPI can be found [here](https://devdocs.io/fastapi/).

### Endpoints

| Method | Endpoint             | Parameters                                             | Defaults | Outputs (Type and Content)                                                                                                                                                                                                                                | Purpose                                                                                                                                   |
|--------|----------------------|--------------------------------------------------------|----------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------|
| POST   | /create-user         | Users Body<br/> ```username```: String<br/> ```password```: String | N/A      | JSONResponse<br/> ```content="Account created successfully. New User Id: {userId}"```                                                                                                                                                                     | Creates both a new user in the database with a hashed password and a player instance for immediate gameplay.                              |
| POST   | /login               | Users Body<br/> ```username```: String<br/> ```password```: String | N/A      | JSONResponse<br/> ```content="Player logged in successfully."```                                                                                                                                                                                          | Logs user in and loads their player stats and data for immediate gameplay.                                                                |
| POST   | /enter-game          | ModeRequest Body<br/> ```mode```: String                     | "NORMAL" | JSONResponse<br/> ```content="Player successfully entered game."```                                                                                                                                                                                       | Enters user into the game by populating the game with the corresponding configurations based on the difficulty mode (defaults to Normal). |
| POST   | /submit-guess        | GuessRequest Body<br/> ```guess```: String                   | N/A      | JSONResponse<br/> ```userId```: String,<br/> ```status```: String,<br/> ```correctNumbers```: Int,<br/> ```correctPositionsAndNumbers```: Int,<br/> ```guess```: String,<br/> ```currentRound```: Int,<br/> ```totalRounds```: Int,<br/> ```isLastRound```: Int,<br/> ```remainingGuesses```: Int | Submits a player's guess for validation and evaluation in order to generate a hint, win, or lose.                                         |
| PUT    | /update-player-stats | PlayerStats Body<br/> ```userId```: String                   | N/A      | JSONResponse<br/> ```content="Player stats updated successfully."```                                                                                                                                                                                      | Updates PlayerStats table with player's new stats located in memory.                                                                      |        |                      |                                                              |          |                                                                                                                                                                                                                                                                                                   |                                                                                                                                           |
| GET    | /get-player-stats    | Query<br/> ```userId```: String                              | N/A      | JSONResponse<br/> PlayerStatsTable                                                                                                                                                                                                                        | Returns player's stats directly from the database as validation to be displayed for the user on the frontend at the end of a game.        |
| POST   | /reset               | None                                                   | N/A      | JSONResponse<br/>  ```content="Game and player have reset."```                                                                                                                                                                                            | Resets both in-memory player instance and game instance for fresh login.                                                                  |

### Sequence Diagram
This sequence diagram starts with the POST /enter-game request, followed by a POST /submit-guess of an incorrect guess. The user then wins on the second POST /submit-guess and the sequence diagram showcases the data traversal across services to update the stats before finally saving to the database.
![APISequenceDiagram](assets/MastermindAPISequenceDiagram.svg)
(Please right-click and open the image in a new tab for greater readability)

## Database
### Schema
The database has three tables: the UsersTable, PlayerStatsTable, and FeatureFlags table. This schema demonstrates the relationship between them and the data and data types they store.<br/>
![Database Schema](assets/MastermindDatabaseSchema.svg)

## Technologies, Code Structure, and Thought Process
### Technologies with Documentation
Mastermind is built in Python for the backend and React for the frontend. Tests are built with Python's built-in unittests.

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
The codebase is separated into two main directories: the `api` and `mastermind-frontend` so that they can be individually deployed and containerized.

- `./api/services` contains the core game logic, including the `PlayMastermindGameService`, configurations, and tests for `__getHint` (`GetHintTests`) and `submitGuess` (`SubmitGuessTests`).
- `./api/features` contains the additional features for this game: `DifficultyModeService`, `LevelUserService`, `PlayerDataManagementService`, and `PlayerStatsManagementService`, along with their individual `DatabaseServices`, Utils, and Tests.
- `./api/clients` contains logic for calling external APIs, such as the `RandomDotOrgAPIClientRequest`
- `./api/database` contains the schema for the various database tables (UsersTable, PlayerStatsTable, and FeatureFlagTable). This is also the location of the generated `.db` file upon running the game.
- In the root api directory, the `app.py` file contains the core API logic, including Body request schemas and endpoints.

#### Frontend
In this game, the frontend is presentational. The only business logic being handled is calling the API endpoints and utilizing the received data to either change state or showcase data to the user.

#### API
The server handles all business/game logic including:
- Dynamically fetching a random sequence from the random.org API based on the user's selected Difficulty Mode configurations.
- Initializing a game instance with the necessary data from the config files.
- Algorithmically comparing the user's guess against the generated sequence from Random.org
- Analyzing whether the guess was a winning or losing condition, updating the client after each guess with roundData so the state can change depending on whether the user has won, lost, or is stillPlaying.
- Updating database with the latest player stats, setting their highestScore, re-calculating their overall experience and winRate, and handling their leveling.
- Querying the database to validate the new data and sending the client parseable data to display it to the user.


### Thought Process
The goal of this project is to develop an application that processes all core logic and data management on the backend, ensuring the frontend remains lightweight and focused solely on user interactions.

The client provides an interface where users can log in, input data, and view feedback or results. It communicates with the backend exclusively via API calls, rendering the data returned from the server. Validation and error handling happen server-side to safeguard against injection attacks, malformed requests, or invalid inputs. The frontend is built for an intuitive user experience, featuring styled, accessible input fields and buttons with a clear purpose.

All critical application logic is centralized on the backend. This includes managing database interactions, handling authentication and authorization, validating inputs, processing business rules, and dynamically generating responses. Core logic is organized into services, ensuring modularity and maintainability. For example:
- Data storage and retrieval are managed via the ORM for scalability.
- Business-critical rules, such as grading or game mechanics, are handled in dedicated service files.
- Responses are dynamically crafted using algorithms and models specific to the application's domain.

The core logic of the game is located in the `PlayMastermindGameService`, which includes the fetching and parsing of the randomly generated winning combination from the `RandomDotOrgAPIClientRequest` upon `enterGame`. When a guess is made, the `PlayMastermindGameService` compares a user's guess to this winning combination using the private `__getHint` method. The `submitGuess` function evaluates whether the condition is a win or a lose and dynamically generates a response to send the user on the client. 

This project is built on SOLID principles, ensuring code clarity and scalability. Endpoints route logic processing to services, while middleware manages cross-cutting concerns like authentication and validation. Try/except blocks wrap critical processes to ensure robust error handling and extensive unit testing ensures the reliability of essential features.


## Future Implementations
### Server
- Implement controllers to call business and DB logic functions within endpoints
- User authentication and authorization using JWT tokens, so sessions expire after a certain amount of time
- Further testing on `PlayMastermindGameService` and corresponding features
- Implement feature flags for each feature and dynamically adjust frontend accordingly
- Consolidate components on the frontend for more universal styles

### Features
#### LevelUserService
- Rewards at specific levels
- Achievements at specific levels

#### Users
- More data collection when creating a user
- Tracking sessionIds for a game session

#### New feature: Input timer
- An input timer that dynamically adjusts based on the difficulty level selected

## Contributions
Please feel free to contribute to this project by either submitting an issue or opening a pull request. All contributions
are welcome and encouraged :).

