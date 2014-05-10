from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask_mail import Mail
from config import SECRET_KEY, MAIL_DEFAULT_SENDER, MAIL_PASSWORD, \
    MAIL_USERNAME

app = Flask(__name__)


### Configure Database and ORM ###

app.config['SQLALCHEMY_DATABASE_URI'] = \
    'postgresql://sagefy:sagefy@localhost/sagefy'
db = SQLAlchemy(app)


### Configure Login ###

app.config['SECRET_KEY'] = SECRET_KEY
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(userid):
    from models.user import User  # TODO: Avoid this
    return User.get_by_id(userid)


## Configure Email ###

app.config['MAIL_DEFAULT_SENDER'] = MAIL_DEFAULT_SENDER
app.config['MAIL_SERVER'] = 'smtp.mandrillapp.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = MAIL_USERNAME
app.config['MAIL_PASSWORD'] = MAIL_PASSWORD
mail = Mail(app)
