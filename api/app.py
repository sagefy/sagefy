from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)

dburi = 'postgresql://sagefy:sagefy@localhost/sagefy'
app.config['SQLALCHEMY_DATABASE_URI'] = dburi
db = SQLAlchemy(app)
