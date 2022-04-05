from re import L
from flask import Flask
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField
from wtforms.validators import InputRequired, Length

"""Forms for note taking app"""

class RegisterUserForm(FlaskForm):
    """ Form to add a new user"""

    username = StringField("Username", validators=[InputRequired(), Length(5, 20)])
    password = PasswordField("Password", validators=[InputRequired(), Length(8, 100)])
    email = EmailField("Email", validators=[InputRequired(), Length(5, 50)])
    first_name = StringField("First Name", validators=[InputRequired(), Length(2, 30)])
    last_name = StringField("Last Name", validators=[InputRequired(), Length(2, 30)])


class LoginForm(FlaskForm):
    """ Form to log user in"""

    username = StringField("Username", validators=[InputRequired(), Length(5, 20)])
    password = PasswordField("Password", validators=[InputRequired(), Length(8, 100)])


class OnlyCsrfForm(FlaskForm):
    """ Form for CSRF protection only """

class AddNoteForm(FlaskForm):
    """ Add a new note for a user """

    title = StringField("Title", validators=[InputRequired(), Length(5, 20)])
