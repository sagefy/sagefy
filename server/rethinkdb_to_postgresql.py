import rethinkdb as r
import psycopg2
from modules.util import convert_slug_to_uuid
from database.util import save_row
from framework.database import make_db_connection

r_db_conn = r.connect(
    host='localhost',
    port=28015,
    db='sagefy',
    timeout=60,
)
pg_db_conn = make_db_connection()

users = r.table('users').run(r_db_conn)

# users - yes

for user in users:
    query = """
        INSERT INTO users
        (id, created, modified, name, email, password, settings)
        VALUES
        (%(id)s, %(created)s, %(modified)s, %(name)s,
         %(email)s, %(password)s, %(settings)s);
    """
    params = {
        'id': convert_slug_to_uuid(user['id']),
        'created': user['created'],  # TODO need to convert to datetime
        'modified': user['modified'],
        'name': user['name'],
        'email': user['email'],
        'password': user['password'],
        'settings': psycopg2.extras.Json(user['settings']),
    }
    save_row(pg_db_conn, query, params)

# TODO generate "dev_data" for cards&params/units/subjects
# units, subjects, cards/params - probably not TODO check if others exist
# topics/posts - probably not TODO check if exist

# notices/follows - skip
# responses - skip

# users_subjects - intro electronic music... TODO others?
for user in users:
    query = """
        INSERT INTO users_subjects
        (user_id, subject_id)
        VALUES
        (%(user_id)s, %(subject_id)s);
    """
    params = {
        'user_id': convert_slug_to_uuid(user['id']),
        'subject_id': '???',  # TODO
    }
    save_row(pg_db_conn, query, params)

r_db_conn.close()
pg_db_conn.close()

# !!! run !es_populate!
