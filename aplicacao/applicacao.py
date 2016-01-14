#-*- coding: utf-8 -*-
import flask, os
from flask import Flask, request, Markup, redirect, g, abort, flash
from aplicacao.models import Usuario, db_session, Banda
from aplicacao.forms import LoginForm, ContactForm
from flask.ext.babel import Babel, gettext
from flask.json import jsonify
from flask.templating import render_template
from aplicacao.utils import requires_auth, buscar_usuario_logado
from aplicacao import config
from flask.helpers import make_response
from flask.ext.mail import Mail, Message

from aplicacao.controller_padrao import padrao
from aplicacao.controller_nocaute import nocaute
from aplicacao.controller import app as blueprintapp

app = Flask(__name__)
app.config.from_pyfile("config.py")

# Initialize Flask-Babel
babel = Babel(app)
E_mail = config.settingEmail(app)

#Caso queira um controller sem o url prefix só não informar ele nos dois lados do blueprint
app.register_blueprint(padrao, url_prefix='/padrao')
app.register_blueprint(nocaute, url_prefix='/nocaute')
app.register_blueprint(blueprintapp)

@babel.localeselector
def get_locale():
    """Define qual a linguagem padrão."""
    #Tradução padrão e obrigatória
    #     return g.get('current_lang', 'pt')
    #O navegador define a melhor tradução
    translations = [str(translation) for translation in babel.list_translations()]
    return request.accept_languages.best_match(translations)

@app.before_request
def before():
    if request.view_args and 'lang_code' in request.view_args:
        if request.view_args['lang_code'] not in ('es', 'en', 'pt'):
            return abort(404)
        g.current_lang = request.view_args['lang_code']
        request.view_args.pop('lang_code')

@app.route('/testemail.do')
def testemail():
    msg = Message(
              'Olá',
           sender='horacio_dias@live.com',
           recipients=
               ['tchdnt@hotmail.com'])
    msg.body = "Corpo do email"
    E_mail.send(msg)
    return "Enviado"

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.teardown_appcontext
def shutdown_session(exception=None):
	db_session.remove()
