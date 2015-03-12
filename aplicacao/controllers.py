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

app = Flask(__name__)
app.config.from_pyfile("config.py")

# Initialize Flask-Babel
babel = Babel(app)
email = config.settingEmail(app)

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


def run():
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port = port)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        usuario_logado = buscar_usuario_logado(form.login.data, form.password.data)
        if usuario_logado:
            flash('Login efetuado')
            response = make_response( redirect('/index'))
            response.set_cookie("autenticacao", value = usuario_logado.cookie)
            return response 
    return flask.render_template('login.html', title='Sign In', form=form)

@app.route('/usuario')
def usuario():
# 	primeiro registro
    retorno = Usuario.query.all()
    if retorno != None and len(retorno) > 0:
        retorno = retorno[0]
        return jsonify(name=retorno.name,login=retorno.login,password=retorno.password,cookie=retorno.cookie,salt=retorno.salt)
    else:
        return ''
    
@app.route('/bandas')
@requires_auth    
def bandas():
    bandas = db_session.query(Banda).all()
    return flask.render_template("bandas.html", bandas = bandas)

@app.route('/')
@app.route('/index')
@app.route('/hello/<name>')
def hello_world(name = None):
    return flask.render_template('teste.html', name = name)
    
@app.route('/marcacao')
def marcacao():
    hello = gettext('Hello World')
#     app.logger.debug("Debug log")
#     app.logger.info("Info log")
#     app.logger.error("Error log")
    #Mostra a tag com a marcacao
    texto1 = Markup('<strong>Hello %s!</strong>') % '<blink>Hacker</blink>'
    #Escapa e mostra o texto com as tag
    texto2 = Markup.escape('<blink>Hacker</blink>')
    #Pula as tags
    texto3 = Markup('<em>Marked up</em> &raquo; HTML').striptags()
    return flask.render_template('marcacao.html', texto1 = texto1, texto2 = texto2, texto3 = texto3, ola = hello )


@app.route('/formulario')
def formulario():
    return flask.render_template('formulario.html')

@app.route('/salvar.do', methods = ["POST"])
def recebe_formulario():
    nome = None
    telefone = None
    if flask.request.method == 'POST':
        nome = flask.request.form['nome']
        telefone = flask.request.form['telefone']
    else:
        return marcacao()
    return flask.render_template('recebe_formulario.html', nome = nome, telefone = telefone)

@app.route('/salvarPorGet.do')
def recebe_por_get():
    nome = None
    telefone = None
    if flask.request.method == 'GET':
        #Se a primeira variavel retornar true so ela e setada caso nao a segunda e setada
        nome = flask.request.args.get('nome') or 'X' 
        telefone = flask.request.args.get('telefone') or ''
    else:
        return marcacao()
    return flask.render_template('recebe_formulario.html', nome = nome, telefone = telefone)

@app.route('/contato.do')
def formulario_contato():
    form = ContactForm()
    if form.validate_on_submit():
        flash('Contato: %s'%(form), 'atributo')
        response = make_response( redirect('/index'))
        return response
    return flask.render_template('formulario_contato.html', form = form)


@app.teardown_appcontext
def shutdown_session(exception=None):
	db_session.remove()
