import rethinkdb as r
import framework.database as database
from framework.database import setup_db, make_db_connection, \
    close_db_connection
from passlib.hash import bcrypt

setup_db()
make_db_connection()

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
    (database.db.table(kind)
        .delete()
        .run(database.db_conn))

(database.db.table('users')
    .insert([{
        'id': 'doris',
        'created': r.now(),
        'modified': r.now(),
        'name': 'doris',
        'email': 'doris@example.com',
        'password': bcrypt.encrypt('example1'),
        'settings': {
            'email_frequency': 'daily',
            'view_sets': 'public',
            'view_follows': 'public',
        }
    }])
    .run(database.db_conn))

(database.db.table('units')
    .insert([{
    }])
    .run(database.db_conn))

(database.db.table('units_parameters')
    .insert([{
    }])
    .run(database.db_conn))

(database.db.table('cards')
    .insert([{
    }])
    .run(database.db_conn))

(database.db.table('cards_parameters')
    .insert([{
    }])
    .run(database.db_conn))

(database.db.table('sets')
    .insert([{
    }])
    .run(database.db_conn))

(database.db.table('sets_parameters')
    .insert([{
    }])
    .run(database.db_conn))

(database.db.table('topics')
    .insert([{
    }])
    .run(database.db_conn))

# TODO proposal .. vote .. flag
(database.db.table('posts')
    .insert([{
    }])
    .run(database.db_conn))

(database.db.table('follows')
    .insert([{
    }])
    .run(database.db_conn))

(database.db.table('notices')
    .insert([{
    }])
    .run(database.db_conn))

(database.db.table('users_sets')
    .insert([{
    }])
    .run(database.db_conn))

(database.db.table('responses')
    .insert([{
    }])
    .run(database.db_conn))

close_db_connection()
