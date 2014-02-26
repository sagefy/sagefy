from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.debug = True

app.config['SQLALCHEMY_DATABASE_URI'] = \
    'postgresql://sagefy:sagefy@localhost/sagefy'
db = SQLAlchemy(app)
