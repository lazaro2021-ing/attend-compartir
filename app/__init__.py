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


user_name='test'
password='test12345'
cluster_name='cluster0'
db_name='present'
proyect_name='i_am_present'


flask_app = Flask(__name__)

flask_app.config['SECRET_KEY'] = '15da6d4asd21a3d1a6s41da1das31da3s2d1a3s2d1a65s1d3a2sd'  
flask_app.config['MONGO_URI']=f'mongodb+srv://{user_name}:{password}@{cluster_name}.hk2bc.mongodb.net/{db_name}?retryWrites=true&w=majority'
flask_app.config['MONGO_DBNAME']=f'{proyect_name}'

mongo=PyMongo(flask_app)




from app.present.routes import mod
from app.home.routes import mod

flask_app.register_blueprint(present.routes.mod,url_prefix='/present')
flask_app.register_blueprint(home.routes.mod)

assets = Environment(flask_app)
assets.init_app(flask_app)
assets.register(bundles)

print(flask_app.url_map)