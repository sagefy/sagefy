import uuid
from database.user import insert_user, \
  update_user, \
  update_user_password, \
  add_user_to_es, \
  get_user, \
  get_user_by_id, \
  get_user_by_email, \
  get_user_by_name, \
  list_users, \
  list_users_by_user_ids, \
  delete_user, \
  deliver_user, \
  is_password_valid, \
  get_avatar, \
  get_learning_context, \
  set_learning_context, \
  get_email_token, \
  is_valid_token
from raw_insert import raw_insert_users
from passlib.hash import bcrypt


user_a_uuid = uuid.uuid4()
user_b_uuid = uuid.uuid4()


def create_test_users(db_conn):
  users = [{
    'id': user_a_uuid,
    'name': 'test',
    'email': 'test@example.com',
    'password': 'abcd1234',
  }, {
    'id': user_b_uuid,
    'name': 'other',
    'email': 'other@example.com',
    'password': 'abcd1234',
  }]
  raw_insert_users(db_conn, users)


def test_insert_user(db_conn):
  data = {
    'name': 'test',
    'email': 'test@example.com',
    'password': 'abcd',
  }
  user, errors = insert_user(db_conn, data)
  assert errors
  assert not user
  data['password'] = 'abcd1234'
  user, errors = insert_user(db_conn, data)
  assert not errors
  assert user


def test_update_user(db_conn):
  create_test_users(db_conn)
  prev_data = get_user_by_id(db_conn, {'id': user_a_uuid})
  assert prev_data
  data = {'email': 'another'}
  user, errors = update_user(db_conn, prev_data, data)
  assert errors
  assert not user
  data = {'email': 'another@example.com'}
  user, errors = update_user(db_conn, prev_data, data)
  assert not errors
  assert user


def test_update_user_password(db_conn):
  create_test_users(db_conn)
  prev_data = get_user_by_id(db_conn, {'id': user_a_uuid})
  assert prev_data
  data = {'password': 'tyui'}
  user, errors = update_user_password(db_conn, prev_data, data)
  assert errors
  assert not user
  data = {'password': 'tyui1234'}
  user, errors = update_user_password(db_conn, prev_data, data)
  assert not errors
  assert user


def test_add_user_to_es(db_conn):
  create_test_users(db_conn)
  user = get_user_by_id(db_conn, {'id': user_a_uuid})
  assert add_user_to_es(user)


def test_get_user(db_conn):
  create_test_users(db_conn)
  assert get_user(db_conn, {'id': user_a_uuid})
  assert get_user(db_conn, {'name': 'test'})
  assert get_user(db_conn, {'email': 'test@example.com'})


def test_get_user_by_id(db_conn):
  create_test_users(db_conn)
  assert get_user_by_id(db_conn, {'id': user_a_uuid})


def test_get_user_by_email(db_conn):
  create_test_users(db_conn)
  assert get_user_by_email(db_conn, {'email': 'test@example.com'})


def test_get_user_by_name(db_conn):
  create_test_users(db_conn)
  assert get_user_by_name(db_conn, {'name': 'test'})


def test_list_users(db_conn):
  create_test_users(db_conn)
  params = {}
  users = list_users(db_conn, params)
  assert len(users) == 2


def test_list_users_by_user_ids(db_conn):
  create_test_users(db_conn)
  user_ids = (user_a_uuid,)
  users = list_users_by_user_ids(db_conn, user_ids)
  assert users
  assert len(users) == 1


def test_delete_user(db_conn):
  create_test_users(db_conn)
  user = get_user_by_id(db_conn, {'id': user_a_uuid})
  add_user_to_es(user)
  assert user
  errors = delete_user(db_conn, user_a_uuid)
  user = get_user_by_id(db_conn, {'id': user_a_uuid})
  assert not errors
  assert not user


def test_deliver_user(db_conn):
  create_test_users(db_conn)
  user = get_user_by_id(db_conn, {'id': user_a_uuid})
  user = deliver_user(user, access=None)
  assert user
  assert not user.get('email')
  assert not user.get('password')
  assert user.get('settings')
  assert not user.get('settings').get('email_frequency')


def test_is_password_valid():
  real_password = 'elephants'
  # NOTE do not set rounds this low in production!
  real_encrypted_password = bcrypt.encrypt(real_password, rounds=4)
  given_password = None
  assert not is_password_valid(real_encrypted_password, given_password)
  given_password = 'monkeys'
  assert not is_password_valid(real_encrypted_password, given_password)
  given_password = real_password
  assert is_password_valid(real_encrypted_password, given_password)


def test_get_avatar():
  email = 'test@example.com'
  avatar_url = get_avatar(email, size=24)
  assert avatar_url
  assert avatar_url.startswith('https://www.gravatar.com/avatar/')
  assert get_avatar('', size=24) == ''
  assert '24' in get_avatar(email, size=0)


def test_get_learning_context(db_conn):
  create_test_users(db_conn)
  user = get_user_by_id(db_conn, {'id': user_a_uuid})
  set_learning_context(user, unit={'entity_id': 'abcd1234'})
  context = get_learning_context(user)
  assert context
  assert context['unit']


def test_set_learning_context(db_conn):
  create_test_users(db_conn)
  user = get_user_by_id(db_conn, {'id': user_a_uuid})
  set_learning_context(user, unit={'entity_id': 'abcd1234'})
  context = get_learning_context(user)
  assert context
  assert context['unit']


def test_get_email_token(db_conn):
  create_test_users(db_conn)
  user = get_user_by_id(db_conn, {'id': user_a_uuid})
  token = get_email_token(user)
  assert token


def test_is_valid_token(db_conn):
  assert not is_valid_token({'id': uuid.uuid4()}, '')
  create_test_users(db_conn)
  user = get_user_by_id(db_conn, {'id': user_a_uuid})
  token = get_email_token(user)
  assert not is_valid_token(user, 'qyzjosinmal1234')
  token = get_email_token(user)
  assert is_valid_token(user, token)
