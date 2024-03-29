from market import db, login_manager
from flask_sqlalchemy import SQLAlchemy
from market import bcrypt
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=30), unique=True, nullable=False)
    email_address = db.Column(db.String(length=50), unique=True, nullable=False)
    password_hash = db.Column(db.String(length=60), nullable=False)
    budget = db.Column(db.Integer(), nullable=False, default=1000)
    items = db.relationship("Item", backref="item_owner", lazy=True)
    
    @property
    def better_budget(self):
        if len(str(self.budget)) > 3:
            return f"{str(self.budget)[:-3]} {str(self.budget)[-3:]}$"
        else:
            return f"{self.budget}$"
    
    @property
    def password(self):
        return self.password
    
    # Connects  User.password_hash to routes.py - new_user password and points to this .setter which hashes the password
    @password.setter
    def password(self, password_to_hash):
        self.password_hash = bcrypt.generate_password_hash(password_to_hash).decode("utf-8")

    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)
    
    def can_purchase(self, item_object):
        return self.budget >= item_object.price
    
    def is_owner(self, item_object_tosell):
        return item_object_tosell in self.items

class Item(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=30), nullable=False, unique=True)
    price = db.Column(db.Integer(), nullable=False)
    barcode = db.Column(db.String(length=20), nullable=False, unique=True)
    description = db.Column(db.String(length=2000), nullable=False, unique=True)
    owner = db.Column(db.Integer(), db.ForeignKey("user.id"))
    
    def __repr__(self):
        return f"Item {self.name}"

    def buy(self, user):
        self.owner = user.id
        user.budget = user.budget - self.price
        db.session.commit()
        
    def sell(self, user):
        self.owner = None
        user.budget = user.budget + self.price
        db.session.commit()
