from flask import Flask, g
from flask.ext.login import LoginManager
from flask_mail import Mail

import rethinkdb as r
from redis import StrictRedis
from elasticsearch import Elasticsearch

from routes.error import setup_errors
from routes.public import public
from routes.user import user
from routes.notice import notice
from routes.topic import topic


def create_app(config, debug=False, testing=False):
    """
    Factory that creates an application instance.
    Setups up all kinds of stuff.
    """

    app = Flask(__name__)

    # Configure the app
    app.config.from_object(config)
    app.debug = debug
    app.testing = testing

    # Setup the database and components
    setup_db(app)
    if not testing:
        setup_conn_per_request(app)
    setup_redis(app)
    setup_search(app)
    setup_login(app)
    setup_email(app)

    # Add in the routes
    setup_errors(app)
    app.register_blueprint(public)
    app.register_blueprint(user)
    app.register_blueprint(notice)
    app.register_blueprint(topic)

    return app


def make_db_connection(app):
    """
    Given a Flask application instance,
    create a database connection.
    """

    db_conn = r.connect(app.config['RDB_HOST'], app.config['RDB_PORT'])
    db = r.db(app.config['RDB_DB'])
    return db_conn, db


def setup_db(app):
    """
    Set up the database.
    Include a sequence to make sure databases and tables exist where they
    need to be.
    """

    db_conn = r.connect(app.config['RDB_HOST'], app.config['RDB_PORT'])

    # Add all setup needed here:
    if app.config['RDB_DB'] not in r.db_list().run(db_conn):
        r.db_create(app.config['RDB_DB']).run(db_conn)

    from models.user import User
    from models.notice import Notice
    from models.topic import Topic
    from models.post import Post
    from models.proposal import Proposal
    from models.vote import Vote
    from models.flag import Flag
    from models.card import Card
    from models.unit import Unit
    from models.set import Set
    from models.follow2 import Follow
    from models.user_sets import UserSets
    from models.response import Response

    models = (User, Notice, Topic, Post, Proposal, Vote, Flag,
              Card, Unit, Set,
              Follow,
              UserSets, Response)

    tables = r.db(app.config['RDB_DB']).table_list().run(db_conn)

    for modelCls in models:
        tablename = getattr(modelCls, 'tablename', None)
        if tablename and tablename not in tables:
            (r.db(app.config['RDB_DB'])
              .table_create(tablename)
              .run(db_conn))
            tables.append(tablename)

        existant_indexes = (r.db(app.config['RDB_DB'])
                             .table(tablename)
                             .index_list()
                             .run(db_conn))
        indexes = getattr(modelCls, 'indexes', [])
        for index in indexes:
            if index[0] not in existant_indexes:
                (r.db(app.config['RDB_DB'])
                  .index_create(*index)
                  .run(db_conn))

    db_conn.close()


def setup_conn_per_request(app):
    """
    On each request, we create and close a new connection.
    Rethink was designed to work this way, no reason to be alarmed.
    """

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
    Store a Redis instance on our app object.
    """

    app.redis = StrictRedis()


def setup_search(app):
    """
    Create an elastic search reference.
    """

    app.es = Elasticsearch()


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
