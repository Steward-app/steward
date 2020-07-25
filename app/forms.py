from flask_wtf import FlaskForm
from wtforms import SubmitField
from wtformsparsleyjs import StringField, PasswordField, BooleanField, SelectField
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
        validators.Regexp('^(?=.*[0-9]+.*)(?=.*[a-zA-Z]+.*)[0-9a-zA-Z!@#$%^&*]{12,72}$', message='Password must contain at least one letter, at least one number, and be longer than 12 charaters.')
        ])
    password_repeat = PasswordField('Password again', validators=[
        validators.DataRequired(),
        validators.EqualTo('password', message='Passwords must match')
        ])
    submit = SubmitField('Create User')

class MaintenanceForm(FlaskForm):
    choices=[('cpp', 'C++'), ('py', 'Python'), ('text', 'Plain Text')]
    assets=[
            ('------', '------'),
            ('Bed', 'Bed'),
            ('Fridge', 'Fridge')
            ]
    schedules=[
            ('------', '------'),
            ('Weekly', 'Weekly'),
            ('Monthly', 'Monthly')
            ]
    name = StringField('Name', validators=[validators.DataRequired()])
    description = StringField('Description')
    asset = SelectField('Asset', choices=assets, validators=[validators.DataRequired()])
    schedule = SelectField('Schedule', choices=schedules, validators=[validators.DataRequired()])
    enabled = BooleanField('Enabled')
    submit = SubmitField()
