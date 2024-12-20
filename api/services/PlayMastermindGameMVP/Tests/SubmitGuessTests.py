from api.services.PlayMastermindGameMVP.PlayMastermindGameService import Mastermind
import unittest
from unittest.mock import AsyncMock, MagicMock
import json

"""
Tests the response object to the frontend by the API when submitting a guess.
"""
class TestMastermindSubmitGuess(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        """ Mock data in preparation for tests """
        self.mockPlayer = MagicMock(userId="testUserId1234", gamesWon=0)
        self.mockLevelingService = MagicMock()
        self.mockPlayerStatsService = AsyncMock()
        self.mockRandomDotOrgAPIClient = AsyncMock()
        self.game = Mastermind(player=self.mockPlayer)
        self.game.randomDotOrgAPIClientRequest = self.mockRandomDotOrgAPIClient
        self.game.playerStatsService = self.mockPlayerStatsService

        # Arrange data
        self.game.winningCombo = "0115"

    async def testSubmitGuessIncorrectRoundOne(self):
        """
        Tests an incorrect guess submission on the first round
        """
        # Arrange
        self.game.roundCounter = 0
        self.game.remainingGuesses = 10
        guess = "1234"

        # Act
        response = await self.game.submitGuess(guess)

        # Assert
        parsedResponse = json.loads(response.body.decode("utf-8"))
        assert parsedResponse["userId"] == self.game.player.userId
        assert parsedResponse["status"] == "stillPlaying"
        assert parsedResponse["correctNumbers"] == "1"
        assert parsedResponse["correctPositionsAndNumbers"] == "0"
        assert parsedResponse["guess"] == guess
        assert parsedResponse["currentRound"] == 1
        assert parsedResponse["totalRounds"] == 10
        assert parsedResponse["isLastRound"] == False
        assert parsedResponse["remainingGuesses"] == 9

    async def testSubmitGuessCorrectRoundOne(self):
        """
        Tests a correct guess submission on the first round
        """
        # Arrange
        self.game.roundCounter = 0
        self.game.remainingGuesses = 10
        guess = "0115"

        # Act
        response = await self.game.submitGuess(guess)

        # Assert
        parsedResponse = json.loads(response.body.decode("utf-8"))
        assert parsedResponse["userId"] == self.game.player.userId
        assert parsedResponse["status"] == "won"
        assert parsedResponse["correctNumbers"] == "4"
        assert parsedResponse["correctPositionsAndNumbers"] == "4"
        assert parsedResponse["guess"] == guess
        assert parsedResponse["currentRound"] == 1
        assert parsedResponse["totalRounds"] == 10
        assert parsedResponse["isLastRound"] == False
        assert parsedResponse["remainingGuesses"] == 9

    async def testSubmitGuessIncorrectLastRound(self):
        """
        Tests an incorrect guess submission on the last round to make sure the user loses
        """
        # Arrange
        self.game.roundCounter = 9
        self.game.remainingGuesses = 1
        guess = "1004"

        # Act
        response = await self.game.submitGuess(guess)

        # Assert
        parsedResponse = json.loads(response.body.decode("utf-8"))
        assert parsedResponse["userId"] == self.game.player.userId
        assert parsedResponse["status"] == "lost"
        assert parsedResponse["correctNumbers"] == "2"
        assert parsedResponse["correctPositionsAndNumbers"] == "0"
        assert parsedResponse["guess"] == guess
        assert parsedResponse["currentRound"] == 10
        assert parsedResponse["totalRounds"] == 10
        assert parsedResponse["isLastRound"] == True
        assert parsedResponse["remainingGuesses"] == 0

    async def testSubmitGuessInvalidGuess(self):
        """
        Tests that an invalid guess submission is caught as a ValueError
        """
        # Arrange
        self.game.roundCounter = 0
        self.game.remainingGuesses = 10
        guess = "543211"

        # Act & Assert
        with self.assertRaises(ValueError) as context:
            await self.game.submitGuess(guess)

        self.assertEqual(str(context.exception), "{'ERROR': 'Guess does not meet requirements.'}")


if __name__ == "__main__":
    unittest.main()
