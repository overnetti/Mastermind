from fastapi import HTTPException
import requests
import logging
import traceback


class RandomDotOrgAPIClientRequest:
    def __init__(self):
        self.RandomDotOrgURL = "https://www.random.org/integers/"

    async def generateWinningCombo(self, inputLength, minRandomDigit, maxRandomDigit):
        # todo: wrap in try/catch
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
