from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
app = Flask(__name__)
app.config.from_pyfile('config.py')
db = SQLAlchemy(app)
CORS(app)

from view import *
from model import Usuarios

#CORS(app, resources={r"/curso": {"origins": "*"}})

CORS(app, origins=["*"])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)