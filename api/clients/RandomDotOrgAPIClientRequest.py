from fastapi import HTTPException
import requests
import logging
import traceback

"""
Handles requests to the Random.org API for generating random number combinations.
"""
class RandomDotOrgAPIClientRequest:
    def __init__(self):
        # Constructs the URL for fetching the randomized sequence
        self.RandomDotOrgURL = "https://www.random.org/integers/"

    async def generateWinningCombo(self, inputLength: int, minRandomDigit: int, maxRandomDigit: int) -> str:
        """
        Generates a randomized winning combination based on the game configuration parameters.
        @param {Int} inputLength - Required length of the combination.
        @param {Int} minRandomDigit - The minimum valid digit in the combination.
        @param {Int} maxRandomDigit - The maximum valid digit in the combination.
        @returns {String} Containing the winning combination.
        @throws {Error} HTTPException: If an error occurs generating the combination, a 500 error is thrown.
        """
        try:
            randomdotorgResponse = requests.get(self.RandomDotOrgURL,
                                                params={'num': inputLength, 'min': minRandomDigit,
                                                        'max': maxRandomDigit, 'col': 1, 'base': 10, 'format': 'plain',
                                                        'rnd': 'new'})
            winningValue = randomdotorgResponse.text
            joinedWinningValue = ''.join(winningValue.split())
        except Exception as e:
            logging.error(f"Error generating winning combination: {traceback.format_exc()}")
            raise HTTPException(status_code=500, detail=str(e))
        return joinedWinningValue
