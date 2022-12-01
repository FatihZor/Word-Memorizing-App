import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or '7soino32noonN@^#iuiuw9'
    DATABASE_CONNECT_OPTIONS = {}
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    RAPIDAPI_KEY = os.environ.get("RAPIDAPI_KEY", "03b058f235msh4586a487cc9934fp1abcacjsn118226d04cd0")
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'app.db')