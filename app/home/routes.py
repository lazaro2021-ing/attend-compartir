from flask import Blueprint,request,render_template,redirect,url_for,flash,jsonify
from flask_assets import Environment, Bundle
from app.config import *
from app import flask_app


mod=Blueprint("home",__name__,static_folder="static",template_folder="templates",static_url_path="/%s" % __name__)



js = Bundle('home/js/background_animate.js',output="gen/all_js.js")
bundles["all_js"]=js

css = Bundle("home/css/style.css","home/css/animate.min.css",output="gen/all_css.css")
bundles["all_css"]=css



@mod.route('/')
@mod.route('/home', methods=['GET','POST'])
def home(): 
    return render_template("home.html")


