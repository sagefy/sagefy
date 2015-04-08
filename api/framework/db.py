"""
On each request, we create and close a new connection.
Rethink was designed to work this way, no reason to be alarmed.
"""

import rethinkdb as r

config = {
    'RDB_HOST': 'localhost',
    'RDB_PORT': 28015,
    'RDB_DB': 'sagefy',
}

db, db_conn = None, None


def make_db_connection():
    """
    Create a database connection.
    """

    db_conn = r.connect(config['RDB_HOST'], config['RDB_PORT'])
    db = r.db(config['RDB_DB'])
    return db_conn, db


def close_db_connection():
    """
    Close the DB connection.
    """
    return db_conn.close()


def setup_db():
    """
    Set up the database.
    Include a sequence to make sure databases and tables exist where they
    need to be.
    """

    db_conn = r.connect(config['RDB_HOST'], config['RDB_PORT'])

    # Add all setup needed here:
    if config['RDB_DB'] not in r.db_list().run(db_conn):
        r.db_create(config['RDB_DB']).run(db_conn)

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
    from models.card_parameters import CardParameters
    from models.unit_parameters import UnitParameters
    from models.set_parameters import SetParameters
    from models.follow import Follow
    from models.user_sets import UserSets
    from models.response import Response

    models = (User, Notice, Topic, Post, Proposal, Vote, Flag,
              Card, Unit, Set,
              CardParameters, UnitParameters, SetParameters,
              Follow, UserSets, Response)

    tables = r.db(config['RDB_DB']).table_list().run(db_conn)

    for modelCls in models:
        tablename = getattr(modelCls, 'tablename', None)
        if tablename and tablename not in tables:
            (r.db(config['RDB_DB'])
              .table_create(tablename)
              .run(db_conn))
            tables.append(tablename)

        existant_indexes = (r.db(config['RDB_DB'])
                             .table(tablename)
                             .index_list()
                             .run(db_conn))
        indexes = getattr(modelCls, 'indexes', [])
        for index in indexes:
            if index[0] not in existant_indexes:
                (r.db(config['RDB_DB'])
                  .index_create(*index)
                  .run(db_conn))

    db_conn.close()
