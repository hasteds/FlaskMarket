from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy
from market.config import Config

app = Flask(__name__)
app.config.from_object(Config)

with app.app_context():
    db = SQLAlchemy(app)
    
from market import routes