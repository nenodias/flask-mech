#-*- coding: utf-8 -*-

WTF_CSRF_ENABLED = True
SECRET_KEY = 'senha-deve-ser-secreta'
SQLALCHEMY_DATABASE_URI = "sqlite:///banco.db"

def settingEmail(app):
    from flask_mail import Mail
    # After 'Create app'
    app.config['MAIL_SERVER'] = 'smtp.example.com'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USE_SSL'] = True
    app.config['MAIL_USERNAME'] = 'username'
    app.config['MAIL_PASSWORD'] = 'password'
    return Mail(app)