# -*- coding: utf-8 -*-
"""
Created on Thu Feb 13 23:41:47 2020

@author: lzr
"""
from app import flask_app


if __name__ == "__main__":
    flask_app.run(debug=True,host = 'localhost',port=5000)

   

