#!/usr/bin/env python3

__version__ = "0.0.1"

from absl import logging
from flask import Flask, render_template, flash, redirect, request
from flask_login import UserMixin, login_user, login_required, logout_user, current_user
import grpc

from urllib.parse import urlparse, urljoin

from steward import user_pb2 as u
from steward import maintenance_pb2 as m
from steward import registry_pb2 as r
from steward import registry_pb2_grpc

from app.assets import assets
from app.forms import LoginForm, CreateUserForm, CreateMaintenanceForm
from app.extensions import lm, mail, bcrypt

app = Flask(__name__)
app.config.from_object('websiteconfig')
assets.init_app(app)
lm.init_app(app)
mail.init_app(app)
bcrypt.init_app(app)


# TODO(artanicus): this hardcodes to the monolithic backend which is bad
channel = grpc.insecure_channel('localhost:50051')
users = registry_pb2_grpc.UserServiceStub(channel)
maintenances = registry_pb2_grpc.MaintenanceServiceStub(channel)

def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
           ref_url.netloc == test_url.netloc

def get_redirect_target():
    for target in request.values.get('next'), request.referrer:
        if not target:
            continue
        if is_safe_url(target):
            return target

@app.route('/')
def root():
    return render_template('index.html', users=users.ListUsers(u.ListUsersRequest()))

@app.route('/maintenances')
@login_required
def list_maintenances():
    return render_template('maintenances.html', maintenances=maintenances.ListMaintenances(m.ListMaintenancesRequest()))

@app.route('/user/<user_id>')
@login_required
def user(user_id=None):
    return render_template('user.html', user=users.GetUser(u.GetUserRequest(_id=user_id)))

@app.route('/maintenance/create', methods=['GET', 'POST'])
@login_required
def maintenance_create():
    form = CreateMaintenanceForm()
    if form.validate_on_submit():
        maintenance = m.Maintenance()
        maintenance.name = form.name.data
        maintenance.description = form.description.data
        new_maintenance = maintenances.CreateMaintenance(maintenance)
        flash('Maintenace \'{}\' Created!'.format(form.name.data))
        return redirect('/maintenance/{}'.format(new_maintenance._id))
    return render_template('maintenance_create.html', form=form)

@app.route('/maintenance/<maintenance_id>')
@login_required
def maintenance(maintenance_id=None):
    return render_template('maintenance.html', maintenance=maintenances.GetMaintenance(m.GetMaintenanceRequest(_id=maintenance_id)))


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        target_user = users.GetUser(u.GetUserRequest(email=form.email.data))
        if bcrypt.check_password_hash(target_user.password, form.password.data):
            logging.warning('login, got from db: {}'.format(form.email.data))
            user = WrappedUser()
            user.load(target_user)
            login_user(user)
            flash('Login succeeded for user {}'.format(form.email.data))

            next = get_redirect_target()
            return redirect(next)
        else:
            flash('Incorrect password')
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = CreateUserForm()
    if form.validate_on_submit():
        user = u.CreateUserRequest()
        user.name = form.name.data
        user.email = form.email.data
        user.password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        users.CreateUser(user)
        flash('User Created for {}'.format(form.email.data))
        return redirect('/')
    return render_template('register.html', form=form)

@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')

@lm.user_loader
def load_user(user_id):
    user = WrappedUser(user_id)
    return user

class WrappedUser(UserMixin):
    def __init__(self, user_id=None):
        if user_id is not None:
            logging.warning('user created by id, got from db: {}'.format(user_id))
            self.user = users.GetUser(u.User(_id=user_id))
    def get_id(self):
        return self.user._id

    def load(self, proto):
        self.user = proto
