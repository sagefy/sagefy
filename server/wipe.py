import rethinkdb as r
from framework.database import setup_db, make_db_connection, \
    close_db_connection
from framework.elasticsearch import es

setup_db()
db_conn = make_db_connection()

for kind in (
    'users',
    'units',
    'units_parameters',
    'cards',
    'cards_parameters',
    'sets',
    'sets_parameters',
    'topics',
    'posts',
    'follows',
    'notices',
    'users_sets',
    'responses',
):
    (r.table(kind)
      .delete()
      .run(db_conn))

es.indices.delete(index='entity', ignore=[400, 404])

close_db_connection(db_conn)
