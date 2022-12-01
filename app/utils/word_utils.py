
from app import db
from app.api.models import Point
def search_word(word: str) -> dict:
    """
    :rtype: dict
    :type word: str
    """
    import requests

    url = "https://wordsapiv1.p.rapidapi.com/words/%s" % word

    headers = {
        "X-RapidAPI-Key": "03b058f235msh4586a487cc9934fp1abcacjsn118226d04cd0",
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