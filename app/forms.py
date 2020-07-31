from flask_wtf import FlaskForm
from wtforms import SubmitField
from wtformsparsleyjs import StringField, PasswordField, BooleanField, SelectField, DateField
from wtforms import validators

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[validators.DataRequired()])
    password = PasswordField('Password', validators=[validators.DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class UserForm(FlaskForm):
    name = StringField('Name', validators=[validators.DataRequired()])
    email = StringField('Email', validators=[
        validators.DataRequired(),
        validators.Email(message="Not a valid email address")
        ])
    old_password = PasswordField('Current Password', validators=[validators.DataRequired()])
    password = PasswordField('Password', validators=[
        validators.DataRequired(),
        validators.Regexp('^(?=.*[0-9]+.*)(?=.*[a-zA-Z]+.*)[0-9a-zA-Z!@#$%^&*]{12,72}$', message='Password must contain at least one letter, at least one number, and be longer than 12 charaters.')
        ])
    password_repeat = PasswordField('Password again', validators=[
        validators.DataRequired(),
        validators.EqualTo('password', message='Passwords must match')
        ])
    submit = SubmitField()

class MaintenanceForm(FlaskForm):
    name = StringField('Name', validators=[validators.DataRequired()])
    description = StringField('Description')
    asset = SelectField('Asset')
    schedule = SelectField('Schedule')
    enabled = BooleanField('Enabled')
    submit = SubmitField()

class AssetForm(FlaskForm):
    name = StringField('Name', validators=[validators.DataRequired()])
    description = StringField('Description')
    organization = StringField('Organization')
    acquired = DateField('Acquired')
    submit = SubmitField()

class DeleteForm(FlaskForm):
    submit = SubmitField(label='Delete')
