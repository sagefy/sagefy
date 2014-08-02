from flask import Flask, g
from flask.ext.login import LoginManager
from flask_mail import Mail
from config import SECRET_KEY, MAIL_DEFAULT_SENDER, MAIL_PASSWORD, \
    MAIL_USERNAME
import rethinkdb as r
from rethinkdb.errors import RqlRuntimeError
import os
from redis import StrictRedis

app = Flask(__name__)

app.debug = True


### Configure Database ###

# From http://rethinkdb.com/docs/examples/flask-backbone-todo/

app.config['RDB_HOST'] = os.environ.get('RDB_HOST') or 'localhost'
app.config['RDB_PORT'] = os.environ.get('RDB_PORT') or 28015
app.config['RDB_DB'] = 'sagefy'


def setup_db():
    db_conn = r.connect(app.config['RDB_HOST'], app.config['RDB_PORT'])

    try:
        r.db_create(app.config['RDB_DB']).run(db_conn)
        r.db(app.config['RDB_DB']).table_create('users').run(db_conn)

    except RqlRuntimeError:
        print 'No need to setup RethinkDB.'

    finally:
        db_conn.close()


@app.before_request
def make_db_connection():
    g.db_conn = r.connect(app.config['RDB_HOST'], app.config['RDB_PORT'])
    g.db = r.db(app.config['RDB_DB'])


@app.teardown_request
def close_db_connection(exception):
    g.db_conn.close()


### Configure Redis ###

app.redis = StrictRedis()


### Configure Login ###

app.config['SECRET_KEY'] = SECRET_KEY
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    from models.user import User  # TODO: Avoid this
    return User.get(id=user_id)


## Configure Email ###

app.config['MAIL_DEFAULT_SENDER'] = MAIL_DEFAULT_SENDER
app.config['MAIL_SERVER'] = 'smtp.mandrillapp.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = MAIL_USERNAME
app.config['MAIL_PASSWORD'] = MAIL_PASSWORD
mail = Mail(app)
