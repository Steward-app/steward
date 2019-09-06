#!/bin/sh
cd app
yarn install --modules-folder static/node_modules 
FLASK_APP=__init__.py flask assets build 
