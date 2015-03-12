from functools import wraps
from aplicacao.database import db_session
from flask import request, Response, redirect
from werkzeug.security import generate_password_hash, check_password_hash
from aplicacao.models import Usuario
from datetime import datetime

def check_auth(username, password):
    """This function is called to check if a username /
    password combination is valid.
    """
    return username == 'admin' and password == 'secret'

def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
    'Could not verify your access level for that URL.\n'
    'You have to login with proper credentials', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        cookie_hash = request.cookies.get('autenticacao')
        usuario_logado = None
        if cookie_hash:
            usuario_logado = buscar_por_hash(cookie_hash)
        if not usuario_logado:
            return redirect('/login')
        return f(*args, **kwargs)
    return decorated

def generate_password(senha, salt):
    return generate_password_hash(senha+salt)

def check_password(clear_password, salt, password_hash):
    return check_password_hash(password_hash, clear_password + salt)

def buscar_por_hash(codigo_hash):
    return db_session.query(Usuario).filter(Usuario.cookie == codigo_hash).first()

def buscar_usuario_logado(login, senha):
    from aplicacao.controllers import app
    usuario_logado = db_session.query(Usuario).filter(Usuario.login == login).first()
    app.logger.info(login+"\n"+senha)
    app.logger.info(usuario_logado)
    if usuario_logado and check_password(senha, usuario_logado.salt, usuario_logado.password):
        cookie_hash = generate_password(str(datetime.now()), usuario_logado.salt)
        usuario_logado.cookie = cookie_hash
        db_session.commit()
        return usuario_logado
    