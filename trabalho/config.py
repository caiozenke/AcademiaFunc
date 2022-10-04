# importações
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

# configurações
app = Flask(__name__)
# caminho do arquivo de banco de dados
path = os.path.dirname(os.path.abspath(__file__))
arquivobd = os.path.join(path, 'teste.db')
# sqlalchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+arquivobd
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)