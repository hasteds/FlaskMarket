from market import app, db
from flask import render_template, redirect, url_for, flash, request
from market.models import Item, User
from market.forms import RegisterForm, LoginForm, PurchaseForm, SellForm
from flask_login import login_user, logout_user, login_required, current_user

@app.route("/")
@app.route("/home")
def home_page():
    return render_template("home.html")


@app.route("/market", methods=["GET", "POST"])
@login_required
def market_page():
    purchase_form = PurchaseForm()
    sell_form = SellForm()
    
    if request.method == "POST":
        # Purchasing of items:
        purchased_item = request.form.get("purchased_item")
        item_obj = Item.query.filter_by(name=purchased_item).first()
        if item_obj is not None:
            if current_user.can_purchase(item_obj):
                item_obj.buy(current_user)
                flash(f"Item: {item_obj.name} purchased succesfully for {item_obj.price}$", category="success")
            else:
                flash(f"You dont have enough money to purchase {item_obj.name}", category="danger")
        
        # Selling of items:
        sold_item = request.form.get("sold_item")
        item_obj_tosell = Item.query.filter_by(name=sold_item).first()
        if item_obj_tosell is not None:
            if current_user.is_owner(item_obj_tosell):
                item_obj_tosell.sell(current_user)
                flash(f"You successfully sold {item_obj_tosell.name} for {item_obj_tosell.price}$", category="success")
            else:
                flash(f"Error, could not sell {item_obj_tosell.name}", category="danger")
        
        return redirect(url_for("market_page"))
    
    if request.method == "GET":
        items = Item.query.filter_by(owner=None)
        owned_items = Item.query.filter_by(owner=current_user.id)
        return render_template("market.html", items=items, purchase_form=purchase_form, owned_items=owned_items, sell_form=sell_form)


@app.route("/register", methods=["GET", "POST"])
def register_page():
    form = RegisterForm()
    
    if form.validate_on_submit():
        new_user = User(username=form.username.data,
                        email_address=form.email.data,
                        password=form.password.data)
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        flash(f"Account created succesfully. You are now loged in as {new_user.username}", category="success")
        return redirect(url_for("market_page"))
    
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f"Error creating user: {err_msg}", category="danger")
    return render_template("register.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        check_user = User.query.filter_by(username=form.username.data).first()
        if check_user and check_user.check_password_correction(attempted_password=form.password.data):
            login_user(check_user)
            flash(f"Successful login. {check_user.username} welcome to the market!", category="success")
            return redirect(url_for("market_page"))
        else:
            flash("Username or password is incorrect. Please try again.", category="danger")
    return render_template("login.html", form=form)


@app.route("/logout")
def logout_page():
    logout_user()
    flash("You have been logged out!", category="info")
    return redirect(url_for("home_page"))