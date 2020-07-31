#!/usr/bin/env python3

__version__ = "0.0.1"

from absl import logging
from flask import Flask, render_template, flash, redirect, request

from app.app_assets import assets
from app.extensions import lm, mail, bcrypt

app = Flask(__name__)
app.config.from_object('websiteconfig')
assets.init_app(app)
lm.init_app(app)
mail.init_app(app)
bcrypt.init_app(app)

from app import user, maintenance, asset
app.register_blueprint(user.bp)
app.register_blueprint(maintenance.bp)
app.register_blueprint(asset.bp)

@app.route('/')
def root():
    return render_template('index.html')
