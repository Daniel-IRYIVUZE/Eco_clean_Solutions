from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config["SECRET_KEY"] = '0981750a37cfe506ff71e37a6cc0d6f3bff4a6c125855f84c8aa932976fc69be'
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///real.db"
db = SQLAlchemy(app)
bcrypt= Bcrypt(app)
login_manager= LoginManager(app)
login_manager.login_view= "login"
login_manager.login_message_category= "info"
from EcoApp import routes