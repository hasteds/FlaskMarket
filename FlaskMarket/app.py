from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///market.db"
with app.app_context():
    db = SQLAlchemy(app)


class Item(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=30), nullable=False, unique=True)
    price = db.Column(db.Integer(), nullable=False)
    barcode = db.Column(db.String(length=20), nullable=False, unique=True)
    description = db.Column(db.String(length=2000), nullable=False, unique=True)
    
    def __repr__(self):
        return f"Item {self.name}"

@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html")


@app.route("/about/<username>")
def about(username):
    return render_template("about.html")


@app.route("/market")
def market_page():
    items = Item.query.all()
    return render_template("market.html", items=items)