'''
Created on 13/03/2015

@author: nenodias
'''
import flask
from flask import Flask, request, Markup, redirect, g, abort, flash, current_app
from flask.templating import render_template

from flask import Blueprint

padrao = Blueprint('padrao', __name__,url_prefix='/padrao')

@padrao.route('/componentes')
def componentes():
    return flask.render_template("padrao/componentes.html")

@padrao.route('/homepage')
def homepage():
    return flask.render_template("padrao/homepage.html")