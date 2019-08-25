#!/usr/bin/env python3

__version__ = "0.0.1"

from absl import logging

from flask import Flask, render_template
app = Flask(__name__)
app.config.from_object('websiteconfig')

users = {
        42: 'pertti',
        666: 'luci'
        }

@app.route('/')
def root():
    return render_template('index.html', users=users)

@app.route('/user/<id>')
def user(id=None):
    return render_template('user.html', user=users[int(id)])
    
