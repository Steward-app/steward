#!/usr/bin/env python3

__version__ = "0.0.1"

from absl import logging
from flask import Flask, render_template, flash, redirect
from flask_assets import Environment, Bundle
import grpc

from steward import user_pb2 as u
from steward import registry_pb2 as r
from steward import registry_pb2_grpc

from app.assets import assets
from app.forms import LoginForm, CreateUserForm

app = Flask(__name__)
app.config.from_object('websiteconfig')
assets.init_app(app)

channel = grpc.insecure_channel('localhost:50051')
users = registry_pb2_grpc.UserServiceStub(channel)

@app.route('/')
def root():
    return render_template('index.html', users=users.ListUsers(u.ListUsersRequest()))

@app.route('/user/<id>')
def user(id=None):
    return render_template('user.html', user=users.GetUser(u.User(_id=id)))

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login Requested for user {}'.format(form.email.data))
        return redirect('/')
    return render_template('login.html', form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = CreateUserForm()
    if form.validate_on_submit():
        user = u.CreateUserRequest()
        user.name = form.name.data
        user.email = form.email.data
        user.password = form.password.data
        users.CreateUser(user)
        flash('User Created for {}'.format(form.email.data))
        return redirect('/')
    return render_template('signup.html', form=form)
