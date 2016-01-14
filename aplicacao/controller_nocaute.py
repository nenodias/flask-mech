'''
Created on 13/03/2015

@author: nenodias
'''
import flask, os
from flask import Flask, request, Markup, redirect, g, abort, flash, current_app, Response
from json import dumps
from flask.json import jsonify
from flask.templating import render_template
from flask.helpers import make_response
from werkzeug import secure_filename

from flask import Blueprint

nocaute = Blueprint('nocaute', __name__,url_prefix='/nocaute')

@nocaute.route('/')
def index():
    return flask.render_template("nocaute/nocaute.html")

@nocaute.route('/form')
def form():
    return flask.render_template("nocaute/nocaute_form.html")

@nocaute.route('/salvar', methods=['GET', 'POST'])
def salvar():
    if request.method == 'POST':  
        json = request.form
        print(json)
        return jsonify(json)
    return make_response( redirect('/nocaute/form'))

@nocaute.route('/tasks')
def tasks():
    lista = [{'title':'LOL', 'isDone':False}]
    return Response(dumps(lista),  mimetype='application/json')


def allowed_file(filename):
    ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@nocaute.route('/upload.do', methods=['GET', 'POST'])
def arquivo():
    if request.method == 'POST':
        UPLOAD_FOLDER = ''
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            flash("Arquivo"+filename)
            return make_response( redirect('/nocaute/upload.do'))
    return render_template("nocaute/nocaute_upload.html")
        