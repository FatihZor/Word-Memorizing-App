from flask import Flask
from app.config import Config
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

bcrypt = Bcrypt()

db = SQLAlchemy()

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    bcrypt.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)

    from app.main.routes import main
    app.register_blueprint(main)

    from app.auth.routes import auth
    app.register_blueprint(auth)

    from app.api.routes import api
    app.register_blueprint(api)


    return app