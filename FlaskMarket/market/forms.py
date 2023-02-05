from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField


class RegisterForm(FlaskForm):
    username = StringField(label="User Name:")
    email = StringField(label="Email Address")
    password = PasswordField(label="Password")
    password_repeat = PasswordField(label="Repeat Password")
    submit = SubmitField(label="Create Account")