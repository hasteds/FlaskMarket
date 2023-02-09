from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError
from market.models import User


class RegisterForm(FlaskForm):
    # Check if username already exist in database, if exist raise validation error
    # .validators library checks for field after underscore(_) in this case it is > username < and runs the function
    def validate_username(self, username_to_check):
        user = User.query.filter_by(username=username_to_check.data).first()
        if user is not None:
            raise ValidationError("Username already exist. Please create new username.")

    # Check if email already exist in database, if exist raise validation error
    def validate_email(self, email_to_check):
        mail = User.query.filter_by(email_address=email_to_check.data).first()
        if mail is not None:
            raise ValidationError("Email already exist. Please create new email adress.")
    
    username = StringField(label="User Name:", validators=[Length(min=2, max=30), DataRequired()])
    email = StringField(label="Email Address", validators=[Email(), DataRequired()])
    password = PasswordField(label="Password", validators=[Length(min=3), DataRequired()])
    password_repeat = PasswordField(label="Repeat Password", validators=[EqualTo("password"), DataRequired()])
    submit = SubmitField(label="Create Account")
    
class LoginForm(FlaskForm):
    username = StringField(label="User Name", validators=[DataRequired()])
    password = PasswordField(label="Password", validators=[DataRequired()])
    submit = SubmitField(label="Sign In")