from flask import Blueprint,request,render_template,redirect,url_for,flash,jsonify
from flask_assets import Environment, Bundle
from app.config import *
import qrcode
import os
from app import flask_app
import base64
import PIL
from io import BytesIO
from app import mongo
from datetime import datetime

mod=Blueprint("present",__name__,static_folder="static",template_folder="templates",static_url_path="/%s" % __name__)


js = Bundle('present/js/main.js',output="gen/present_all_js.js")
bundles["present_all_js"]=js

'''
css = Bundle("present/css/present.css","present/css/generar.css",output="gen/present_all_css.css")
bundles["present_all_css"]=css

css = Bundle("present/css/confirm.css",output="gen/confirm_all_css.css")
bundles["confirm_all_css"]=css

css = Bundle("present/css/consult.css",output="gen/consult_all_css.css")
bundles["consult_all_css"]=css
'''


@mod.route('/', methods=['GET','POST'])
def index(): 
    print(mod.__dict__)
    return render_template("present.html")

@mod.route('/generar', methods=['GET','POST'])
def generar(): 
    data_req={'clase':request.form["clase"],'email':request.form["mail"],'time':request.form["time"],'institucion':request.form["institucion"]}
    #mandar a una base de datos
    data_hash=str(hash(jsonify(data_req)))
    qr = qrcode.QRCode(version=1,border=0,box_size=8)
    url=f'https://attendlzr.herokuapp.com/present/confirmar?hash={data_hash}'
    qr.add_data(url)
    img=qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    qr_base64 = base64.b64encode(buffered.getvalue())

    now = datetime.now().strftime("%Y-%m-%d")
   
    existing_user = mongo.db.user.find_one({"email":data_req['email']})
    if existing_user == None:
        data_insert={"email":data_req['email'],"present_hash":[]}
        data_insert['present_hash'].append({'hash':data_hash,'institucion':data_req['institucion'],'clase':data_req['clase'],'expiracion':now+' '+data_req['time']})
        mongo.db.user.insert_one(data_insert)
        mongo.db.hash_keys.insert_one({'hash':data_hash,'alumnos':[]})
    else:
        
        data_insert={'hash':data_hash,'institucion':data_req['institucion'],'clase':data_req['clase'],'expiracion':now+' '+data_req['time']}
        mongo.db.user.find_one_and_update({"email":data_req['email']},{"$addToSet":{'present_hash': data_insert }})
        mongo.db.hash_keys.insert_one({'hash':data_hash,'alumnos':[]})
        

    return  render_template('generar.html' ,qr=qr_base64.decode("utf-8"),url=url)

@mod.route('/confirmar', methods=['GET','POST'])
def confirmar(): 
    hash_key=request.args.get('hash')
   
    if request.method=='POST':
        hash_key=request.form["hash"]
        name=request.form["name"]
        
        hash_key_db=mongo.db.hash_keys.find_one({"hash":hash_key})
        now=datetime.now().strftime("%Y-%m-%d %H:%M")
        
        
        hash_key_db['alumnos'].append({'name':name,'time':now})
        mongo.db.hash_keys.find_one_and_update({"hash":hash_key},{"$set":{'alumnos': hash_key_db['alumnos'] }})

    
    
    return render_template('confirmar.html',hash=hash_key)



@mod.route('/consultar', methods=['GET','POST'])
def consultar(): 
    
   
    if request.method=='POST':
        
        mail=request.form["mail"]
        materia=request.form["clase"]
        institucion=request.form["institucion"]
        print(mail,materia,institucion)
        user = mongo.db.user.find_one({"email":mail})
        print(user)

        filter_user=[{'hash':k['hash'],'date':k['expiracion'].split(' ')[0]} for k in user['present_hash'] if k['institucion']==institucion and k['clase']==materia]
        print(filter_user)
        filter_hash={}
        for hash_k in filter_user:
            print(hash_k['hash'])
            consulta=mongo.db.hash_keys.find_one({"hash":hash_k['hash']})
            print(consulta)
            filter_hash[hash_k['hash']]={'alumnos':[]}
            filter_hash[hash_k['hash']]['alumnos']=[c['name'] for c in consulta['alumnos']]
            filter_hash[hash_k['hash']]['date']=hash_k['date']
            
        print(filter_hash)
        return render_template('consult.html',filter_hash=filter_hash,institucion=institucion,materia=materia)

    return render_template('consult.html')