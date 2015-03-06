'''
Created on 05/03/2015

@author: hdias
'''
import json
from aplicacao.database import *
from sqlalchemy import Column, Integer, String, Sequence, ForeignKey, create_engine
from sqlalchemy.orm import relationship, backref

class Usuario(Base):
    __tablename__ = 'users'
    id = Column(Integer, Sequence('user_id_seq'), primary_key = True)
    name = Column(String(50))
    fullname = Column(String(50))
    password = Column(String(12))
    addresses = relationship("Address", order_by = "Address.id", backref = "user")

    def __repr__(self):
        return "<Usuario(name='%s', fullname='%s', password='%s')>" % (self.name, self.fullname, self.password)

class Address(Base):
    __tablename__ = 'addresses'
    id = Column(Integer, primary_key=True)
    email_address = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))
    # user = relationship("Usuario", back_populates="addresses")
    # user = relationship("Usuario", back_populates="addresses")
    def __repr__(self):
        return "<Address(email_address='%s')>" % self.email_address


def run():
    #Criando a tabela
    Base.metadata.create_all(engine)
    

    ed_user = Usuario(name = 'ed', fullname = 'Ed Jones', password = 'edspassword')
    db_session.add(ed_user)
    print "Novo na sessao"
    print db_session.new
    db_session.commit()

    ed_user.password = 'eitagiovana'
    print "Falta atualizar"
    print db_session.dirty
    db_session.commit()
    print ed_user
    jack = Usuario(name='jack', fullname='Jack Bean', password='gjffdd')
    jack.addresses = [Address(email_address='jack@google.com'),Address(email_address='j25@yahoo.com')]

    db_session.add(jack)

    print "Novo na sessao"
    print db_session.new
    db_session.commit()