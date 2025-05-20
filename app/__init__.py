from flask import Flask
import os
from .config import Config
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate 
from flask_cors import CORS
from flask_jwt_extended import JWTManager


app = Flask(__name__)
#app.config.from_object(Config)
app.config.from_object('app.config.Config')
app.config["JWT_SECRET_KEY"] = "super-secret-key"
jwt = JWTManager(app)

CORS(app, origins=os.getenv("ALLOWED_ORIGINS"))

db = SQLAlchemy(app)
# Instantiate Flask-Migrate library here
migrate = Migrate(app, db) 

# Flask-Login login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

from app import views