from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from config import SECRET_KEY

app = Flask(__name__)

app.debug = True

app.config['SQLALCHEMY_DATABASE_URI'] = \
    'postgresql://sagefy:sagefy@localhost/sagefy'
db = SQLAlchemy(app)


app.config['SECRET_KEY'] = SECRET_KEY
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(userid):
    from models.user import User  # TODO: Avoid this
    return User.get_by_id(userid)
