from api.services.PlayMastermindGameMVP.PlayMastermindGameService import Mastermind
import unittest
from unittest.mock import MagicMock


class MastermindGetHintTest(unittest.TestCase):
    def setUp(self):
        self.mockPlayer = MagicMock()
        self.game = Mastermind(player=self.mockPlayer)

    def testGetHint(self):
        """
        Generic functionality test.
        """
        # Arrange
        winningCombo = "1234"
        guess = "1243"

        # Act
        result = self.game._Mastermind__getHint(guess, winningCombo)

        # Assert
        expected_result = {
            "correctPositionAndNumber": 2,
            "correctNumbers": 4
        }
        self.assertEqual(result, expected_result)

    def testGetHintWithRepeatingNumbers(self):
        """
        Ensure repeating numbers in guess are accounted for and the minimum value is output.
        """
        # Arrange
        winningCombo = "1003"
        guess = "3373"

        # Act
        result = self.game._Mastermind__getHint(guess, winningCombo)

        # Assert
        expected_result = {
            "correctPositionAndNumber": 1,
            "correctNumbers": 1
        }
        self.assertEqual(result, expected_result)

    def testGetHintWithMultipleRepeatingNumbers(self):
        """
        Test whether multiple repeating numbers are accounted for properly.
        """
        # Arrange
        winningCombo = "1033"
        guess = "0073"

        # Act
        result = self.game._Mastermind__getHint(guess, winningCombo)

        # Assert
        expected_result = {
            "correctPositionAndNumber": 2,
            "correctNumbers": 2
        }
        self.assertEqual(result, expected_result)

    def testCorrectGuess(self):
        """
        Test that a winning guess is reflected accurately.
        """
        # Arrange
        winningCombo = "1235"
        guess = "1235"

        # Act
        result = self.game._Mastermind__getHint(guess, winningCombo)

        # Assert
        expected_result = {
            "correctPositionAndNumber": 4,
            "correctNumbers": 4
        }
        self.assertEqual(result, expected_result)

    def testIncorrectGuess(self):
        """
        Test that an entirely incorrect guess is reflected accurately.
        """
        # Arrange
        winningCombo = "1235"
        guess = "0707"

        # Act
        result = self.game._Mastermind__getHint(guess, winningCombo)

        # Assert
        expected_result = {
            "correctPositionAndNumber": 0,
            "correctNumbers": 0
        }
        self.assertEqual(result, expected_result)

    def testLongNumberSequence(self):
        """
        Test example #4 from the challenge prompt.
        """
        # Arrange
        winningCombo = "0135012341"
        guess = "0135012341"

        # Act
        result = self.game._Mastermind__getHint(guess, winningCombo)

        # Assert
        expected_result = {
            "correctPositionAndNumber": 10,
            "correctNumbers": 10
        }
        self.assertEqual(result, expected_result)

    def testPromptExampleOne(self):
        """
        Test example #1 from the challenge prompt.
        """
        # Arrange
        winningCombo = "0135"
        guess = "2246"

        # Act
        result = self.game._Mastermind__getHint(guess, winningCombo)

        # Assert
        expected_result = {
            "correctPositionAndNumber": 0,
            "correctNumbers": 0
        }
        self.assertEqual(result, expected_result)

    def testPromptExampleTwo(self):
        """
        Test example #2 from the challenge prompt.
        """
        # Arrange
        winningCombo = "0135"
        guess = "0246"

        # Act
        result = self.game._Mastermind__getHint(guess, winningCombo)

        # Assert
        expected_result = {
            "correctPositionAndNumber": 1,
            "correctNumbers": 1
        }
        self.assertEqual(result, expected_result)

    def testPromptExampleThree(self):
        """
        Test example #3 from the challenge prompt.
        """
        # Arrange
        winningCombo = "0135"
        guess = "2211"

        # Act
        result = self.game._Mastermind__getHint(guess, winningCombo)

        # Assert
        expected_result = {
            "correctPositionAndNumber": 0,
            "correctNumbers": 1
        }
        self.assertEqual(result, expected_result)

    def testPromptExampleFour(self):
        """
        Test example #4 from the challenge prompt.
        """
        # Arrange
        winningCombo = "0135"
        guess = "0156"

        # Act
        result = self.game._Mastermind__getHint(guess, winningCombo)

        # Assert
        expected_result = {
            "correctPositionAndNumber": 2,
            "correctNumbers": 3
        }
        self.assertEqual(result, expected_result)


if __name__ == "__main__":
    unittest.main()
