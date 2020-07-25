#!/usr/bin/env python3

from absl import logging
from flask import Blueprint, render_template, flash, redirect, request
from flask_login import login_required, current_user

from app.forms import CreateUserForm

import grpc
from steward import registry_pb2_grpc
from steward import user_pb2 as u


bp = Blueprint("user", __name__)
logging.set_verbosity(logging.INFO)

channel = grpc.insecure_channel('localhost:50051')
users = registry_pb2_grpc.UserServiceStub(channel)



@bp.route('/user/<user_id>')
@login_required
def user(user_id=None):
    return render_template('user.html', user=users.GetUser(u.GetUserRequest(_id=user_id)))


@bp.route('/profile')
@login_required
def profile():
    return render_template('profile.html')
