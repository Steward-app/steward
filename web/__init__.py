#!/usr/bin/env python3

__version__ = "0.0.1"

from absl import logging
from flask import Flask, render_template
import grpc

from steward import user_pb2 as u
from steward import registry_pb2 as r
from steward import registry_pb2_grpc


app = Flask(__name__)
app.config.from_object('websiteconfig')

channel = grpc.insecure_channel('localhost:50051')
users = registry_pb2_grpc.UserServiceStub(channel)

@app.route('/')
def root():
    return render_template('index.html', users=users.ListUsers(u.ListUsersRequest()))

@app.route('/user/<id>')
def user(id=None):
    return render_template('user.html', user=users.GetUser(u.User(_id=id)))

