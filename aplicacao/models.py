#-*- coding: utf-8 -*-
'''
Created on 05/03/2015

@author: hdias
'''
import json
from aplicacao.database import *
from sqlalchemy import Column, Integer, String, Sequence, ForeignKey, create_engine, Table
from sqlalchemy.orm import relationship, backref, mapper, relation
from wtforms.ext.sqlalchemy.orm import Form
import aplicacao

metadata = Base.metadata

tabela_bandas = Table('bandas', metadata,
    Column('id', Integer, Sequence('bandas_id_seq'), primary_key = True),
    Column('nome', String),
    Column('lugar', String)
)

tabela_discos = Table('discos', metadata,
    Column('id', Integer, Sequence('discos_id_seq'), primary_key = True),
    Column('nome', String),
    Column('ano', Integer)
)

tabela_discos_bandas = Table('discos_bandas', metadata,
    Column('id', Integer, Sequence('discos_bandas_id_seq'),primary_key = True),
    Column('id_banda', Integer, ForeignKey('bandas.id')),
    Column('id_disco', Integer, ForeignKey('discos.id')),
)

tabela_musicas = Table('musicas', metadata,
    Column('id', Integer, Sequence('musicas_id_seq'), primary_key = True),
    Column('id_disco', Integer, ForeignKey('discos.id')),
    Column('id_banda', Integer, ForeignKey('bandas.id')),
    Column('numero', Integer),
    Column('nome', String)
)

class Musica(object):
    def __repr__(self, *args, **kwargs):
        numero = self.numero or 0
        nome = self.nome or ''
        if self.disco:
            disco = self.disco
        else:
            disco = ''
        return "Numero: %i, Nome: %s, Disco: %d"%(numero, nome, disco)
    
mapper(Musica, tabela_musicas)

class Banda(object):
    def __repr__(self, *args, **kwargs):
        nome = self.nome or ''
        lugar = self.lugar or ''
        return "Nome: %s, Lugar: %s"%(nome, lugar)

#Mapeando o Objeto com a tabela
mapper(Banda, tabela_bandas, properties = {"musicas":relation(Musica, backref = "banda" )})

class Disco(object):
    def __repr__(self, *args, **kwargs):
        nome = self.nome or ''
        ano = self.ano or 0
        if self.bandas:
            banda = ','.join([i.nome for i in self.bandas])
        else:
            banda = ''
        return "Nome: %s, Ano: %s, Banda: %s" %(nome, str(ano), banda)
    
mapper(Disco, tabela_discos, properties = {"musicas": relation(Musica, backref = 'disco'), "bandas":relation(Banda, secondary = tabela_discos_bandas, backref = "discos")})

class Usuario(Base):
    __tablename__ = 'users'
    id = Column(Integer, Sequence('user_id_seq'), primary_key = True)
    name = Column(String(50), nullable = False)
    login = Column(String(50), nullable = False)
    salt = Column(String(100), nullable = False)
    password = Column(String(200), nullable = False)
    cookie = Column(String(100), nullable = False)
    addresses = relationship("Address", order_by = "Address.id", backref = "user",uselist=True)

    def __repr__(self):
        return "<Usuario(name='%s', login='%s', password='%s')>" % (self.name, self.login, self.password)

class Address(Base):
    __tablename__ = 'addresses'
    id = Column(Integer, primary_key=True)
    email_address = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))
#     user = relationship("Usuario", backref = 'users.id',lazy='selected', single_parent=True,uselist=False,viewonly=True)
    # user = relationship("Usuario", back_populates="addresses")
    def __repr__(self):
        return "<Address(email_address='%s')>" % self.email_address


def run():
    #Criando a tabela
#     from aplicacao.utils import generate_password
#     Base.metadata.create_all(engine)
#     senha = generate_password("123", "salte")
#     ed_user = Usuario(name = 'neno', login = 'nenodias', salt = "salte", cookie = 'hjsdaiuhsaiudhusa', password = senha)
#     db_session.add(ed_user)
#     print "Novo na sessao"
#     print db_session.new
#     db_session.commit()
# 
#     ed_user.password = 'eitagiovana'
#     print "Falta atualizar"
#     print db_session.dirty
#     db_session.commit()
#     print ed_user
#     jack = Usuario(name='jack', fullname='Jack Bean', password='gjffdd')
#     jack.addresses = [Address(email_address='jack@google.com'),Address(email_address='j25@yahoo.com')]
# 
#     db_session.add(jack)
# 
#     print "Novo na sessao"
#     print db_session.new
#     db_session.commit()
      
#     db_session
#     nova_banda = Banda()
#     nova_banda.nome = "Tankard"
#     nova_banda.lugar = "Frankfurt"
#      
#      
#     db_session.add(nova_banda)
#     db_session.commit()
#     novo_disco = Disco()
#     
#     uma_banda = db_session.query(Banda).filter(Banda.nome == "Tankard").first()
#     
#     novo_disco.nome = "The Morning After"
#     novo_disco.ano = 1988
#     db_session.add(novo_disco)
#     db_session.commit()
#     musicas = ['Intro', 'Commandment', 'Shit-faced', 'TV Hero', 'F.U.N.',
#                'Try Again', 'The Morning After', 'Desperation',
#                'Feed the Lohocla', 'Help Yourself', 'Mon Cheri', 'Outro']
#     i = 1
#     for m in musicas:
#         nova_musica = Musica()
#         nova_musica.nome = m
#         nova_musica.banda = uma_banda
#         nova_musica.numero = i
#         i += 1
# #         Lembra do relation(), backref e tal que falei la em cima? Entao, olha ai!
# #         O atributo nova_musica.disco ai embaixo foi criado com eles. 
#         nova_musica.disco = novo_disco
#         db_session.add(nova_musica)
#         db_session.commit()
#     
#     #Usando novamente um atributo criado na configuracao do mapper...
#     uma_banda.discos.append(novo_disco)
#     
#     #Bom, vamos cadastrar mais umas coisas ai pra entender direitinho como funciona.
#     rdp = Banda()
#     rdp.nome = u"Ratos de Porao"
#     rdp.lugar = u"Sao Paulo"
#     
#     cl = Banda()
#     cl.nome = u"Colera"
#     cl.lugar = u"Sao Paulo"
#     
#     pk = Banda()
#     pk.nome = u"Psykoze"
#     pk.lugar = u"Sao Paulo"
#     
#     fc = Banda()
#     fc.nome = u"Fogo Cruzado"
#     fc.lugar = u"Sao Paulo"
#     
#     outro_disco = Disco()
#     outro_disco.nome = "Sub"
#     outro_disco.bandas.append(rdp)
#     outro_disco.bandas.append(cl)
#     outro_disco.bandas.append(pk)
#     outro_disco.bandas.append(fc)
#     db_session.add(outro_disco)
#     
#     musicas_sub = [(u'Parasita', rdp), (u'Vida Ruim', rdp), (u"Poluição Atômica", rdp),
#                (u"X.O.T.", cl), (u"Bloqueio Mental", cl),
#                (u"Quanto Vale a Liberdade", cl), (u"Terceira Guerra Mundial", pk),
#                (u"Buracos Suburbanos", pk), (u"Fim do Mundo", pk),
#                (u"Desemprego", fc), (u"União entre os Punks do Brasil", fc),
#                (u"Delinqüentes", fc), (u"Não Podemos Falar", rdp),
#                (u"Realidades da Guerra", rdp), (u"Porquê?", rdp), (u"Histeria", cl),
#                (u"Zero zero", cl), (u"Sub-ratos", cl), (u"Vítimas da Guerra", pk),
#                (u"Alienação do Homem", pk), (u"Desilusão", pk), (u"Inimizade", fc),
#                (u"Punk Inglês", fc), (u"Terceira Guerra", fc)]
# 
#     i = 1
#     for m in musicas_sub:
#         nova_musica = Musica()
#         nova_musica.nome = m[0]
#         nova_musica.banda = m[1]
#         nova_musica.numero = i
#         db_session.add(nova_musica)
#         db_session.commit()
#         nova_musica.disco = outro_disco
#         i += 1
        
    #Fim do cadastro
    
    bandas = db_session.query(Banda).all()
    for b in bandas:
        print "Banda: " , b.nome
        for d in b.discos:
            print "  Disco: ", d.nome
            for m in d.musicas:
                if m.banda.id == b.id:
                    print "    Música: ", m.nome