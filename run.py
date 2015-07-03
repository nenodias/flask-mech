#!/usr/bin/env python
#-*- coding: utf-8 -*-

'''
#Detalhe a pasta com as traduções deve se chamar translates

#Comando que extrai as mensagens usadas no projeto
pybabel extract -F babel.cfg -o messages.pot . 

#Comando que cria uma nova tradução
lingua é uma chave com dois caracteres
pybabel init -i messages.pot -d translations -l <lingua>

#Comando que compila as mensagens
pybabel compile -d translations


'''
import os
from aplicacao.applicacao import app
from aplicacao.database import init_db

init_db()

if __name__ == '__main__':
	port = int(os.environ.get("PORT", 8000))
	app.run(debug=True, host='0.0.0.0', port = port)