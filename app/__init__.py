# -*- coding: utf-8 -*-
"""
Created on Thu Feb 13 23:44:15 2020

@author: lzr
"""

from flask import Flask,render_template,request,redirect,url_for,jsonify,Response,flash
import os
from flask_assets import Environment, Bundle
from app.config import *
from flask_pymongo import PyMongo


flask_app = Flask(__name__)
flask_app.config['SECRET_KEY'] = ''  
flask_app.config['MONGO_URI']=''
flask_app.config['MONGO_DBNAME']=""

mongo=PyMongo(flask_app)




from app.present.routes import mod
from app.home.routes import mod

flask_app.register_blueprint(present.routes.mod,url_prefix='/present')
flask_app.register_blueprint(home.routes.mod)

assets = Environment(flask_app)
assets.init_app(flask_app)
assets.register(bundles)

print(flask_app.url_map)