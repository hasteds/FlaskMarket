import os

class Config(object):
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///market.db"
    SECRET_KEY = "0341febe13e7b1011ad6ed17"