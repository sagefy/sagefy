"""
On each request, we create and close a new connection.
Rethink was designed to work this way, no reason to be alarmed.
"""

import rethinkdb as r

config = {
    'rdb_host': 'localhost',
    'rdb_port': 28015,
    'rdb_db': 'sagefy',
}


def make_db_connection():
    """
    Create a database connection.
    """

    return r.connect(
        host=config['rdb_host'],
        port=config['rdb_port'],
        db=config['rdb_db'],
        timeout=60
    )


def close_db_connection(db_conn):
    """
    Close the DB connection.
    """

    db_conn.close()


def setup_db():
    """
    Set up the database.
    Include a sequence to make sure databases and tables exist where they
    need to be.
    """

    db_conn = make_db_connection()

    # add all setup needed here:
    if config['rdb_db'] not in r.db_list().run(db_conn):
        r.db_create(config['rdb_db']).run(db_conn)

    tables = r.db(config['rdb_db']).table_list().run(db_conn)

    from models.topic import Topic
    from models.post import Post
    from models.proposal import Proposal
    from models.vote import Vote
    from models.card import Card
    from models.unit import Unit
    from models.set import Set
    from models.card_parameters import CardParameters

    models = (Topic, Post, Proposal, Vote,
              Card, Unit, Set,
              CardParameters,)

    for model_cls in models:
        tablename = getattr(model_cls, 'tablename', None)
        if tablename and tablename not in tables:
            (r.db(config['rdb_db'])
              .table_create(tablename)
              .run(db_conn))
            tables.append(tablename)

        existant_indexes = (r.db(config['rdb_db'])
                             .table(tablename)
                             .index_list()
                             .run(db_conn))
        indexes = getattr(model_cls, 'indexes', [])
        for index in indexes:
            if index[0] not in existant_indexes:
                (r.db(config['rdb_db'])
                  .index_create(*index)
                  .run(db_conn))

    from schemas.user import schema as user_schema
    from schemas.notice import schema as notice_schema
    from schemas.follow import schema as follow_schema
    from schemas.response import schema as response_schema
    from schemas.user_sets import schema as user_sets_schema
    schemas = (user_schema, notice_schema, follow_schema, response_schema,
               user_sets_schema,)
    for schema in schemas:
        tablename = schema['tablename']

        if tablename and tablename not in tables:
            (r.db(config['rdb_db'])
              .table_create(tablename)
              .run(db_conn))
            tables.append(tablename)

    close_db_connection(db_conn)
