import json, flask
from flask import Flask, request, Markup
from aplicacao.models import Usuario, db_session
from flask.json import jsonify
from flask.templating import render_template



app = Flask(__name__)

@app.route('/usuario')
def usuario():
# 	primeiro registro
	retorno = Usuario.query.all()[0]
	return retorno.name

@app.route('/')
@app.route('/index.do')
@app.route('/hello/<name>')
def hello_world(name = None):
    return flask.render_template('teste.html', name = name)

@app.route('/marcacao')
def marcacao():
    app.logger.debug("Debug log")
    app.logger.info("Info log")
    app.logger.error("Error log")
    #Mostra a tag com a marcacao
    texto1 = Markup('<strong>Hello %s!</strong>') % '<blink>Hacker</blink>'
    #Escapa e mostra o texto com as tag
    texto2 = Markup.escape('<blink>Hacker</blink>')
    #Pula as tags
    texto3 = Markup('<em>Marked up</em> &raquo; HTML').striptags()
    return flask.render_template('marcacao.html', texto1 = texto1, texto2 = texto2, texto3 = texto3 )


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

def run():
	app.debug = True
	app.run()

@app.teardown_appcontext
def shutdown_session(exception=None):
	db_session.remove()