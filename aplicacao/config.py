#-*- coding: utf-8 -*-

WTF_CSRF_ENABLED = True
SECRET_KEY = 'senha-deve-ser-secreta'
SQLALCHEMY_DATABASE_URI = "sqlite:///banco.db"

def settingEmail(app):
    from flask_mail import Mail
    # After 'Create app'
    app.config.update(
    #EMAIL SETTINGS
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=465,
    MAIL_USE_SSL=True,
    MAIL_USERNAME = 'email@gmail.com',
    MAIL_PASSWORD = 'senhadoemail',
    )
    return Mail(app)
