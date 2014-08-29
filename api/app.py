from flask import Flask, g
import rethinkdb as r
from redis import StrictRedis
from flask.ext.login import LoginManager
from flask_mail import Mail

from controllers.error import setup_errors
from controllers.public import public
from controllers.user import user


def create_app(config, debug=False, testing=False):
    """
    Factory that creates an application instance.
    Setups up all kinds of stuff.
    It's fun!
    """
    app = Flask(__name__)

    # Configure the app
    app.config.from_object(config)
    app.debug = debug
    app.testing = testing

    # Setup the database and components
    setup_db(app)
    setup_redis(app)
    setup_login(app)
    setup_email(app)

    # Add in the controllers
    setup_errors(app)
    app.register_blueprint(public)
    app.register_blueprint(user)

    return app


def make_db_connection(app):
    """
    Given a Flask application instance,
    creates a database connection.
    """
    db_conn = r.connect(app.config['RDB_HOST'], app.config['RDB_PORT'])
    db = r.db(app.config['RDB_DB'])
    return db_conn, db


def setup_db(app):
    """
    Sets up the database.
    Includes a sequence to make sure databases and tables exist where they
    need to be.
    """
    db_conn = r.connect(app.config['RDB_HOST'], app.config['RDB_PORT'])

    # Add all setup needed here:
    if app.config['RDB_DB'] not in r.db_list().run(db_conn):
        r.db_create(app.config['RDB_DB']).run(db_conn)

    tables = r.db(app.config['RDB_DB']).table_list().run(db_conn)
    for table in ['users', 'notifications']:
        if table not in tables:
            r.db(app.config['RDB_DB']).table_create(table).run(db_conn)

    db_conn.close()

    # On each request, we create and close a new connection
    # Rethink was designed to work this way, no reason to be alarmed.
    @app.before_request
    def _m():
        # We wrap it here so that we can
        # make the main function available for testing
        g.db_conn, g.db = make_db_connection(app)

    @app.teardown_request
    def _c(*args, **kwargs):
        # Same situation here, we want to be able to
        # test the same way
        g.db_conn.close()


def setup_redis(app):
    """
    Stores a Redis instance on our app object.
    """
    app.redis = StrictRedis()


def setup_login(app):
    """
    Add login capabilities to our app.
    """
    login_manager = LoginManager()
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        from models.user import User  # TODO: Avoid this
        return User.get(id=user_id)


def setup_email(app):
    """
    Add email capabilities to our app.
    """
    app.mail = Mail(app)
