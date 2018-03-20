import urllib
import hashlib
import json
import uuid

from framework.elasticsearch_conn import es
from framework.redis_conn import red
from framework.mail import send_mail
from schemas.user import schema as user_schema
from passlib.hash import bcrypt
from database.util import insert_row, update_row, get_row, list_rows, \
  delete_row, deliver_fields
from modules.util import pick, compact_dict, json_serial, \
  json_prep, convert_slug_to_uuid, convert_uuid_to_slug


# TODO-2 should we use this to test passwords?
# https://github.com/dropbox/python-zxcvbn

WELCOME_TEXT = """
Welcome to Sagefy!

If you did not create this account, please reply immediately.

If you are interested in biweekly updates on Sagefy's progress,
sign up at https://sgef.cc/devupdates

Thank you!
"""

TOKEN_TEXT = """
To change your password, please visit {url}

If you did not request a password change, please reply immediately.
"""

PASSWORD_TEXT = """
You updated your Sagefy password.

If you did not change your password, please reply immediately.
"""


def insert_user(db_conn, data):
  """
  Save the user to the database.
  """

  schema = user_schema
  query = """
    INSERT INTO users
    (  name  ,   email  ,   password  ,   settings  )
    VALUES
    (%(name)s, %(email)s, %(password)s, %(settings)s)
    RETURNING *;
  """
  data = {
    'name': data.get('name', '').lower().strip(),
    'email': data.get('email', '').lower().strip(),
    'password': data.get('password', ''),
    'settings': {
      'email_frequency': 'daily',
      'view_subjects': 'private',
      'view_follows': 'private',
    },
  }
  data, errors = insert_row(db_conn, schema, query, data)
  if not errors:
    add_user_to_es(data)
    send_mail(
      subject='Welcome to Sagefy',
      recipient=data['email'],
      body=WELCOME_TEXT,
    )
  return data, errors


def update_user(db_conn, prev_data, data):
  """
  Update the user. Does not update password!
  """

  schema = user_schema
  query = """
    UPDATE users
    SET name = %(name)s, email = %(email)s, settings = %(settings)s
    WHERE id = %(id)s
    RETURNING *;
  """
  data = {
    'id': convert_slug_to_uuid(prev_data['id']),
    'name': data.get('name', '').lower().strip() or None,
    'email': data.get('email', '').lower().strip() or None,
    'settings': data.get('settings'),
  }
  data, errors = update_row(db_conn, schema, query, prev_data, data)
  if not errors:
    add_user_to_es(data)
  return data, errors


def update_user_password(db_conn, prev_data, data):
  """
  Update the user's password
  """

  schema = user_schema
  query = """
    UPDATE users
    SET password = %(password)s
    WHERE id = %(id)s
    RETURNING *;
  """
  data = {
    'id': convert_slug_to_uuid(prev_data['id']),
    'password': data['password'],
  }
  data, errors = update_row(db_conn, schema, query, prev_data, data)
  if not errors:
    send_mail(
      subject='Sagefy - Password Updated',
      recipient=data['email'],
      body=PASSWORD_TEXT,
    )
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
    id=convert_uuid_to_slug(data['id']),
  )


def get_user(db_conn, params):
  """
  Facade over id v email.
  """

  if params.get('id'):
    return get_user_by_id(db_conn, params)
  if params.get('email'):
    return get_user_by_email(db_conn, params)
  if params.get('name'):
    return get_user_by_name(db_conn, params)


def get_user_by_id(db_conn, params):
  """
  Get the user by ID.
  """

  query = """
    SELECT *
    FROM users
    WHERE id = %(id)s
    LIMIT 1;
  """
  params = {
    'id': convert_slug_to_uuid(params['id']),
  }
  return get_row(db_conn, query, params)


def get_user_by_email(db_conn, params):
  """
  Get the user by email.
  """

  query = """
    SELECT *
    FROM users
    WHERE email = %(email)s
    LIMIT 1;
  """
  params = {
    'email': params['email'],
  }
  return get_row(db_conn, query, params)


def get_user_by_name(db_conn, params):
  """
  Get the user by name.
  """

  query = """
    SELECT *
    FROM users
    WHERE name = %(name)s
    LIMIT 1;
  """
  params = {
    'name': params['name'],
  }
  return get_row(db_conn, query, params)


def list_users(db_conn, params):
  """
  Get a list of _all_ users of Sagefy.
  """

  query = """
    SELECT *
    FROM users
    ORDER BY created DESC;
    /* TODO OFFSET LIMIT */
  """
  params = {}
  return list_rows(db_conn, query, params)


def list_users_by_user_ids(db_conn, user_ids):
  """
  Get a list of users by their user id.
  """

  query = """
    SELECT *
    FROM users
    WHERE id in %(user_ids)s
    ORDER BY created DESC;
    /* TODO OFFSET LIMIT */
  """
  user_ids = tuple([
    convert_slug_to_uuid(user_id)
    for user_id in user_ids
  ])
  params = {
    'user_ids': user_ids,
  }
  return list_rows(db_conn, query, params)


def delete_user(db_conn, user_id):
  """
  Delete a user.
  """
  query = """
    DELETE FROM users
    WHERE id = %(id)s;
  """
  params = {
    'id': user_id,
  }
  errors = delete_row(db_conn, query, params)
  if not errors:
    es.delete(
      index='entity',
      doc_type='user',
      id=convert_uuid_to_slug(user_id),
    )
  return errors


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
  if not size:
    size = 24
  hash_ = hashlib.md5(email.lower().encode('utf-8')).hexdigest()
  params = urllib.parse.urlencode({'d': 'mm', 's': str(size)})
  gravatar_url = "https://www.gravatar.com/avatar/" + hash_ + "?" + params
  return gravatar_url


def get_learning_context(user):
  """
  Get the learning context of the user.
  """

  key = 'learning_context_{id}'.format(id=convert_uuid_to_slug(user['id']))
  try:
    context = json.loads(red.get(key).decode())
  except:
    context = {}
  return context


def set_learning_context(user, **d):
  """
  Update the learning context of the user.

  Keys: `card`, `unit`, `subject`
    `next`: `method` and `path`
  """

  context = get_learning_context(user)
  d = pick(d, ('card', 'unit', 'subject', 'next'))
  context.update(d)
  context = compact_dict(context)
  key = 'learning_context_{id}'.format(id=convert_uuid_to_slug(user['id']))
  red.setex(key, 10 * 60, json.dumps(context, default=json_serial))
  return context


def get_email_token(user):
  """
  Create an email token for the user to reset their password.
  """

  token = convert_uuid_to_slug(uuid.uuid4())
  slugged_user_id = convert_uuid_to_slug(user['id'])
  red.setex(
    'user_password_token_{id}'.format(id=slugged_user_id),  # key
    60 * 10,  # time
    bcrypt.encrypt(slugged_user_id + token)  # value
  )
  url = '%(base)spassword?id=%(id)s&token=%(token)s' % {
    'base': 'https://sagefy.org/',
    'id': slugged_user_id,
    'token': token,
  }
  send_mail(
    subject='Sagefy - Reset Password Request',
    recipient=user['email'],
    body=TOKEN_TEXT.replace('{url}', url)
  )
  return token


def is_valid_token(user, token):
  """
  Ensure the given token is valid.
  """

  slugged_user_id = convert_uuid_to_slug(user['id'])
  key = 'user_password_token_{id}'.format(id=slugged_user_id)
  entoken = red.get(key)
  red.delete(key)
  if entoken:
    entoken = entoken.decode()
    return bcrypt.verify(slugged_user_id + token, entoken)
  return False
