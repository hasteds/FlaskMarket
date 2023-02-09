from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy
from market.config import Config
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object(Config)

with app.app_context():
    db = SQLAlchemy(app)
    bcrypt = Bcrypt(app)
    login_manager = LoginManager(app)
    login_manager.login_view = "login_page"
    login_manager.login_message_category = "info"
    
from market import routes