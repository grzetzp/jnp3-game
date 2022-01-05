from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, EqualTo

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField("Login")


class RegisterForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    repeat_password = PasswordField("Repeat passoword", validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField("Regsiter")


class User():
    def __init__(self, username, password_hash):
        self.username = username
        self.password_hash = password_hash


def login_valid(username, password, user_db):
    return username == user_db['username'] and password == user_db['password']

def log_out(resp, session):
    resp.set_cookie('username', '', expires=0)
    session.clear()
    return