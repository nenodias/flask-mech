#-*- coding: utf-8 -*-

from flask.ext.wtf import Form
from wtforms import StringField, BooleanField, TextField, PasswordField, validators
from wtforms.validators import DataRequired
from wtforms.fields.core import IntegerField, FormField

class LoginForm(Form):
    login = TextField('login', [validators.Length(min=4, max=25)])
    password = PasswordField('New Password', [
        validators.Required(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')
    
class TelephoneForm(Form):
    country_code = IntegerField('Country Code', [validators.required()])
    area_code    = IntegerField('Area Code/Exchange', [validators.required()])
    number       = TextField('Number')

class ContactForm(Form):
    first_name   = TextField()
    last_name    = TextField()
    mobile_phone = FormField(TelephoneForm)
    office_phone = FormField(TelephoneForm)