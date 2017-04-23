from schemas.user import schema as user_schema
import urllib
import hashlib
from passlib.hash import bcrypt
from database.util import insert_document, update_document, \
    get_document, deliver_fields
from framework.elasticsearch import es
import json
from framework.redis import redis
from modules.util import uniqid, pick, compact_dict, json_serial, \
    omit, json_prep
from modules.content import get as c
from framework.mail import send_mail
import rethinkdb as r

# TODO-2 should we use this to test passwords?
# https://github.com/dropbox/python-zxcvbn


def insert_user(data, db_conn):
    """
    Save the user to the database.
    """

    schema = user_schema
    data, errors = insert_document(schema, data, db_conn)
    if not errors:
        add_user_to_es(data)
    return data, errors


def update_user(prev_data, data, db_conn):
    """
    Overwrite update method to remove password.
    """

    schema = user_schema
    data = omit(data, ('password',))
    data, errors = update_document(schema, prev_data, data, db_conn)
    if not errors:
        add_user_to_es(data)
    return data, errors


def update_user_password(prev_data, data, db_conn):
    """
    Overwrite update method to add password.
    """

    schema = user_schema
    data = pick(data, ('password',))
    data, errors = update_document(schema, prev_data, data, db_conn)
    return data, errors


def add_user_to_es(user):
    """
    Add the user to Elasticsearch.
    """

    data = json_prep(deliver_user(user))
    data['avatar'] = get_avatar(user['email'])

    return es.index(
        index='entity',
        doc_type='user',
        body=data,
        id=data['id'],
    )


def get_user(params, db_conn):
    """
    Get the user matching the parameters.
    """

    tablename = user_schema['tablename']
    return get_document(tablename, params, db_conn)


def list_users(params, db_conn):
    """
    Get a list of users of Sagefy.
    """

    schema = user_schema
    query = r.table(schema['tablename'])
    return list(query.run(db_conn))

# def delete_user(doc_id, db_conn):
#     """
#     Overwrite delete method to delete in Elasticsearch.
#     """
#
#     # TODO-2 should we validate the delete worked before going to ES?
#     tablename = user_schema['tablename']
#     es.delete(
#         index='entity',
#         doc_type='user',
#         id=doc_id,
#     )
#     return delete_document(tablename, doc_id, db_conn)


def deliver_user(data, access=None):
    """
    Prepare user data for JSON response.
    """

    schema = user_schema
    return deliver_fields(schema, data, access)


def is_password_valid(real_encrypted_password, given_password):
    """
    Take an encrypted password, and verifies it. Returns bool.
    """

    try:
        return bcrypt.verify(given_password, real_encrypted_password)
    except:
        return False


def get_avatar(email, size=24):
    """
    Gets the avatar for the given user.
    """

    if not email:
        return ''

    hash_ = hashlib.md5(email.lower().encode('utf-8')).hexdigest()
    params = urllib.parse.urlencode({'d': 'mm', 's': str(size)})
    gravatar_url = "https://www.gravatar.com/avatar/" + hash_ + "?" + params
    return gravatar_url


def get_learning_context(user):
    """
    Get the learning context of the user.
    """

    key = 'learning_context_{id}'.format(id=user['id'])
    try:
        context = json.loads(redis.get(key).decode())
    except:
        context = {}
    return context


def set_learning_context(user, **d):
    """
    Update the learning context of the user.

    Keys: `card`, `unit`, `set`
        `next`: `method` and `path`
    """

    context = get_learning_context(user)
    d = pick(d, ('card', 'unit', 'set', 'next'))
    context.update(d)
    context = compact_dict(context)
    key = 'learning_context_{id}'.format(id=user['id'])
    redis.setex(key, 10 * 60, json.dumps(context, default=json_serial))
    return context


def get_email_token(user, send_email=True):
    """
    Create an email token for the user to reset their password.
    """

    token = uniqid()
    redis.setex(
        'user_password_token_{id}'.format(id=user['id']),  # key
        60 * 10,  # time
        bcrypt.encrypt(user['id'] + token)  # value
    )
    if send_email:
        send_mail(
            subject='Sagefy - Reset Password',
            recipient=user['email'],
            body=c('change_password_url').replace(
                '{url}',
                '%spassword?id=%s&token=%s' %
                ('https://sagefy.org/', user['id'], token)
            )
        )
    return token


def is_valid_token(user, token):
    """
    Ensure the given token is valid.
    """

    key = 'user_password_token_{id}'.format(id=user['id'])
    entoken = redis.get(key)
    redis.delete(key)
    if entoken:
        entoken = entoken.decode()
        return bcrypt.verify(user['id'] + token, entoken)
    return False
