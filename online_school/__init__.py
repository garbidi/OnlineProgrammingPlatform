from flask import Flask
from flask_login import LoginManager, UserMixin, current_user, login_user, logout_user, login_required

from pymongo import MongoClient
from flask_restful import Api

app = Flask(__name__)
app.config["SECRET_KEY"] = 'hnjfnejb4jhbb5jb5bj4nybjbghhfg'
api = Api(app)

app.config.update(
    SESSION_COOKIE_SECURE=True,  # Устанавливает флаг Secure в cookies
    SESSION_COOKIE_HTTPONLY=True,  # Устанавливает флаг HttpOnly в cookies
    SESSION_COOKIE_SAMESITE='Strict',  # Устанавливает атрибут SameSite в cookies
    PERMANENT_SESSION_LIFETIME=3600  # Срок действия сессии в секундах (1 час)
)


db_client = MongoClient('mongodb://localhost:27017/')
db = db_client['online-school']

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'