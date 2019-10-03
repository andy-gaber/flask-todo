from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager


app = Flask(__name__)           # App Initialization
app.config.from_object(Config)  # Configuration
db = SQLAlchemy(app)            # Database Initialization
migrate = Migrate(app, db)      # DB Migration Initialization
login = LoginManager(app)       # Login Manager


from app import routes, models, errors
