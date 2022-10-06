# importações
from http import server
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from flask import Flask, jsonify, request, session
from flask_session import Session
import datetime
from datetime import timedelta
from flask_cors import CORS

# configurações
app = Flask(__name__)

server = "http://127.0.0.1:5000" 
# caminho do arquivo de banco de dados
path = os.path.dirname(os.path.abspath(__file__))
arquivobd = os.path.join(path, 'teste.db')
# sqlalchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+arquivobd
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)