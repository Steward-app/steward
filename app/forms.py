from flask_wtf import FlaskForm
from wtforms import SubmitField
from wtformsparsleyjs import StringField, PasswordField, BooleanField
from wtforms import validators

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[validators.DataRequired()])
    password = PasswordField('Password', validators=[validators.DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class CreateUserForm(FlaskForm):
    name = StringField('Name', validators=[validators.DataRequired()])
    email = StringField('Email', validators=[validators.DataRequired(), validators.Email(message="Not a valid email address")])
    password = PasswordField('Password', validators=[
        validators.DataRequired(),
        validators.Length(min=12)
        ])
    password_repeat = PasswordField('Password again', validators=[
        validators.DataRequired(),
        validators.EqualTo('password', message='Passwords must match')
        ])
    submit = SubmitField('Create User')

class CreateMaintenanceForm(FlaskForm):
    name = StringField('Name', validators=[validators.DataRequired()])
    description = StringField('Description')
    submit = SubmitField('Create Maintenance')
