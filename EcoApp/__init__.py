from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SECRET_KEY"] = '0981750a37cfe506ff71e37a6cc0d6f3bff4a6c125855f84c8aa932976fc69be'
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///eco.db"
db = SQLAlchemy(app)