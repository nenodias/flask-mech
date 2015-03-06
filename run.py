from aplicacao import app
from aplicacao.database import init_db

init_db()

if __name__ == '__main__':
    app.run()