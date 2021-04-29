from flask import Blueprint,request,render_template,redirect,url_for,flash,jsonify
from flask_assets import Environment, Bundle
from app.config import *
from app import flask_app


mod=Blueprint("home",__name__,static_folder="static",template_folder="templates",static_url_path="/%s" % __name__)


'''
js = Bundle('present/js/main.js',output="gen/present_all_js.js")
bundles["present_all_js"]=js
'''
css = Bundle("home/css/home.css","home/css/animate.min.css",output="gen/all_css.css")
bundles["all_css"]=css



@mod.route('/')
@mod.route('/home', methods=['GET','POST'])
def home(): 
    return render_template("home.html")


