from market import app
from flask import render_template
from market.models import Item, User

@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html")


@app.route("/market")
def market_page():
    items = Item.query.all()
    return render_template("market.html", items=items)