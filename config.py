
import os, secrets
from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)


app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY") or "dev-" + secrets.token_hex(32)


db = SQLAlchemy(app)
CORS(app)


app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL", "sqlite:///grova.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
migrate = Migrate(app, db)
