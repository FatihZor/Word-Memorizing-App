
from app import db
from app.api.models import Point
import requests
from app.config import Config
def search_word(word: str) -> dict:
    """
    :rtype: dict
    :type word: str
    """

    url = "https://wordsapiv1.p.rapidapi.com/words/%s" % word

    headers = {
        "X-RapidAPI-Key": Config.RAPIDAPI_KEY,
        "X-RapidAPI-Host": "wordsapiv1.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers)

    print(response.json())

    return response.json()

def add_word_point(user_id, word_id, point=1, reason=""):
    """
    :type user_id: int
    :type word_id: int
    :type point: int
    :type reason: str
    """
    
    _point = Point(
        user_id=user_id,
        word_id=word_id,
        point=point,
        reason=reason
    )

    db.session.add(_point)
    db.session.commit()