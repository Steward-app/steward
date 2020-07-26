#!/usr/bin/env python3

__version__ = "0.0.1"

from absl import logging
from flask import Flask, render_template, flash, redirect, request
import grpc

from urllib.parse import urlparse, urljoin

from steward import user_pb2 as u
from steward import maintenance_pb2 as m
from steward import registry_pb2_grpc

from app.app_assets import assets
from app.forms import LoginForm, CreateUserForm, MaintenanceForm
from app.extensions import lm, mail, bcrypt

app = Flask(__name__)
app.config.from_object('websiteconfig')
assets.init_app(app)
lm.init_app(app)
mail.init_app(app)
bcrypt.init_app(app)

from app import auth, user, maintenance, asset
app.register_blueprint(auth.bp)
app.register_blueprint(user.bp)
app.register_blueprint(maintenance.bp)
app.register_blueprint(asset.bp)

# TODO(artanicus): this hardcodes to the monolithic backend which is bad
channel = grpc.insecure_channel('localhost:50051')
users = registry_pb2_grpc.UserServiceStub(channel)

logging.set_verbosity(logging.INFO)

@app.route('/')
def root():
    return render_template('index.html', users=users.ListUsers(u.ListUsersRequest()))
