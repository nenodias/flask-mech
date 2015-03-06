from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base




# create_engine('postgresql://postgres:postgres@localhost:5432/banco', echo=True)
#                dialect+driver://username:password@host:port/database
# engine = create_engine('sqlite:///:memory:', echo = True)
# engine = create_engine('postgresql://postgres:postgres@localhost:5432/banco', echo=True)
engine = create_engine('sqlite:///banco.db', echo=True)
db_session = scoped_session(sessionmaker(autocommit = False, autoflush = False, bind = engine))
Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    # import all modules here that might define modelos so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    from aplicacao import models
    Base.metadata.create_all(bind = engine)
    models.run()