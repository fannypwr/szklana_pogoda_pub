from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Email, EqualTo

from app.models import User

ALREADY_REGISTERED = 'Such email has been already registered!'
CONFIRM_PASS = 'Confirm your password'
LOG_IN = 'Log in'
DONT_MATCH = 'Passwords don\'t match'
REGISTER = 'Register'
YOUR_EMAIL = 'Your email'
YOUR_PASS = 'Your password'


class LoginForm(FlaskForm):
    email = StringField(YOUR_EMAIL, validators=[DataRequired(), Email()])
    password = PasswordField(YOUR_PASS, validators=[DataRequired()])
    submit = SubmitField(LOG_IN)


class RegisterForm(FlaskForm):
    email = StringField(YOUR_EMAIL, validators=[DataRequired(), Email()])
    password = PasswordField(YOUR_PASS, validators=[DataRequired()])
    confirm_password = PasswordField(CONFIRM_PASS, validators=[DataRequired(),
                                     EqualTo('password', message=DONT_MATCH)])
    submit = SubmitField(REGISTER)

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError(ALREADY_REGISTERED)