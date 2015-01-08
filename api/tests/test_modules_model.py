import pytest

xfail = pytest.mark.xfail


from modules.model import Model
from modules.validations import is_required, is_email, has_min_length
from datetime import datetime


def encrypt_password(value):
    if value and not value.startswith('$2a$'):
        return '$2a$' + value


class User(Model):
    tablename = 'users'

    schema = dict(Model.schema.copy(), **{
        'name': {
            'validate': (is_required,),
            'unique': True,
        },
        'email': {
            'validate': (is_required, is_email),
            'unique': True,
            'access': 'private'
        },
        'password': {
            'validate': (is_required, (has_min_length, 8)),
            'access': False,
            'bundle': encrypt_password
        }
    })


def test_table_class(app, db_conn, users_table):
    """
    Expect the model to have a table as a class.
    """
    assert User.tablename == 'users'
    assert User.table == users_table


@xfail
def test_create_instance(app, db_conn, users_table):
    """
    Expect to create a model instance. Be able to pass in data too...
    """
    return False


def test_table_instance(app, db_conn, users_table):
    """
    Expect the model to have a table as an instance.
    """
    user = User()
    assert user.tablename == 'users'
    assert user.table == users_table


@xfail
def test_get_item(app, db_conn, users_table):
    """
    Expect to get an item from the model.
    """
    return False


@xfail
def test_set_item(app, db_conn, users_table):
    """
    Expect to set an item in the model.
    """
    return False


@xfail
def test_del_item(app, db_conn, users_table):
    """
    Expect to remove an item in the model.
    """
    return False


@xfail
def test_has_item(app, db_conn, users_table):
    """
    Expect to test if model has an item.
    """
    return False


def test_get_id(app, db_conn, users_table):
    """
    Expect to be able to retrieve a model by ID.
    """
    users_table.insert({
        'id': 'abcdefgh12345678',
        'name': 'test',
        'email': 'test@example.com',
    }).run(db_conn)
    user = User.get(id='abcdefgh12345678')
    assert user['name'] == 'test'


def test_get_params(app, db_conn, users_table):
    """
    Expect a model to retrieve by params.
    """
    users_table.insert({
        'id': 'abcdefgh12345678',
        'name': 'test',
        'email': 'test@example.com',
    }).run(db_conn)
    user = User.get(name='test', email='test@example.com')
    assert user['id'] == 'abcdefgh12345678'


def test_get_none(app, db_conn, users_table):
    """
    Expect a no model when `get` with no match.
    """
    users_table.insert({
        'id': 'abcdefgh12345678',
        'name': 'test',
        'email': 'test@example.com',
    }).run(db_conn)
    user = User.get(id='87654321hgfedcba')
    assert user is None


def test_list(app, db_conn, users_table):
    """
    Expect to get a list of models.
    """
    users_table.insert([
        {
            'id': '1',
            'name': 'test1',
            'email': 'test1@example.com',
        },
        {
            'id': '2',
            'name': 'test2',
            'email': 'test2@example.com',
        },
        {
            'id': '3',
            'name': 'test3',
            'email': 'test3@example.com',
        },
    ]).run(db_conn)
    users = User.list()
    assert len(users) == 3
    assert isinstance(users[0], User)
    assert users[2]['id'] in ('1', '2', '3')


def test_list_params(app, db_conn, users_table):
    """
    Expect to get a list of models by params.
    """
    users_table.insert([
        {
            'id': '1',
            'name': 'test1',
            'email': 'test1@example.com',
        },
        {
            'id': '2',
            'name': 'test2',
            'email': 'test2@example.com',
        },
        {
            'id': '3',
            'name': 'test3',
            'email': 'test3@example.com',
        },
    ]).run(db_conn)
    users = User.list(id='1', name='test1')
    assert len(users) == 1
    assert users[0]['email'] == 'test1@example.com'


def test_list_none(app, db_conn, users_table):
    """
    Expect to get an empty list of models when none.
    """
    users = User.list()
    assert len(users) == 0


def test_generate_id(app, db_conn, users_table):
    """
    Expect to automatically generate an ID.
    """
    user = User({'password': 'abcd1234'})
    d = user.bundle()
    assert isinstance(d['id'], str)
    assert len(d['id']) == 24


@xfail
def test_validate(app, db_conn, users_table):
    """
    Expect to validate a model.
    """
    return False


@xfail
def test_bundle(app, db_conn, users_table):
    """
    Expect to...
    """
    return False


@xfail
def test_default(app, db_conn, users_table):
    """
    Expect to...
    """
    return False


@xfail
def test_deliver(app, db_conn, users_table):
    """
    Expect to...
    """
    return False


@xfail
def test_access(app, db_conn, users_table):
    """
    Expect to...
    """
    return False


def test_insert(app, db_conn, users_table):
    """
    Expect to create a new model instance.
    """
    user, errors = User.insert({
        'name': 'test',
        'email': 'test@example.com',
        'password': 'abcd1234'
    })
    assert len(errors) == 0
    record = list(users_table.filter({'name': 'test'}).run(db_conn))[0]
    assert user['id']
    assert user['name'] == 'test'
    assert record['email'] == 'test@example.com'


def test_insert_fail(app, db_conn, users_table):
    """
    Expect to error on failed create model.
    """
    assert len(list(users_table.run(db_conn))) == 0
    user, errors = User.insert({
        'email': 'test@example.com'
    })
    assert user['name'] is None
    assert user['password'] is None
    assert isinstance(user, User)
    assert isinstance(errors, (list, tuple))
    assert len(errors) == 2
    assert errors[0]['message']


def test_update(app, db_conn, users_table):
    """
    Expect to update a model instance.
    """
    user, errors = User.insert({
        'name': 'test',
        'email': 'test@example.com',
        'password': 'abcd1234'
    })
    assert len(errors) == 0
    user, errors = user.update({
        'email': 'open@example.com'
    })
    assert len(errors) == 0
    record = list(users_table.filter({'name': 'test'}).run(db_conn))[0]
    assert user['email'] == 'open@example.com'
    assert record['email'] == 'open@example.com'


def test_update_fail(app, db_conn, users_table):
    """
    Expect to error on failed update model instance.
    """
    user, errors = User.insert({
        'name': 'test',
        'email': 'test@example.com',
        'password': 'abcd1234'
    })
    assert len(errors) == 0
    user, errors = user.update({
        'email': 'open'
    })
    record = list(users_table.filter({'name': 'test'}).run(db_conn))[0]
    assert isinstance(user, User)
    assert isinstance(errors, (list, tuple))
    assert user['email'] == 'open'
    assert record['email'] == 'test@example.com'


def test_save(app, db_conn, users_table):
    """
    Expect a model to be able to save at any time.
    """
    user = User({
        'name': 'test',
        'email': 'test@example.com',
        'password': 'abcd1234'
    })
    user, errors = user.save()
    assert len(errors) == 0
    records = list(users_table.filter({'name': 'test'}).run(db_conn))
    assert len(records) == 1


def test_delete(app, db_conn, users_table):
    """
    Expect to delete a model.
    """
    user, errors = User.insert({
        'name': 'test',
        'email': 'test@example.com',
        'password': 'abcd1234'
    })
    assert len(errors) == 0
    user.delete()
    records = list(users_table.filter({'name': 'test'}).run(db_conn))
    assert len(records) == 0


def test_id_keep(app, db_conn, users_table):
    """
    Expect a model to maintain an ID.
    """
    user, errors = User.insert({
        'name': 'test',
        'email': 'test@example.com',
        'password': 'abcd1234'
    })
    id = user['id']
    user.update({
        'name': 'other'
    })
    assert user['id'] == id


def test_created(app, db_conn, users_table):
    """
    Expect a model to add created time.
    """
    user, errors = User.insert({
        'name': 'test',
        'email': 'test@example.com',
        'password': 'abcd1234'
    })
    record = list(users_table.filter({'name': 'test'}).run(db_conn))[0]
    assert record['created'] == user['created']


def test_transform(app, db_conn, users_table):
    """
    Expect a model to call transform before going into DB.
    """
    user, errors = User.insert({
        'name': 'test',
        'email': 'test@example.com',
        'password': 'abcd1234'
    })
    assert len(errors) == 0
    assert user['password'].startswith('$2a$')


def test_modified(app, db_conn, users_table):
    """
    Expect to sync fields with database.
    """
    user, errors = User.insert({
        'name': 'test',
        'email': 'test@example.com',
        'password': 'abcd1234'
    })
    user, errors = user.update({
        'email': 'other@example.com'
    })
    record = list(users_table.filter({'name': 'test'}).run(db_conn))[0]
    assert isinstance(user['modified'], datetime)
    assert record['modified'] == user['modified']
    assert user['created'] != user['modified']


def test_unique(app, db_conn, users_table):
    """
    Expect a validation to test uniqueness.
    """
    user, errors = User.insert({
        'name': 'test',
        'email': 'test@example.com',
        'password': 'abcd1234',
    })
    user2, errors2 = User.insert({
        'name': 'test',
        'email': 'coin@example.com',
        'password': '1234abcd',
    })
    assert len(errors) == 0
    assert len(errors2) == 1
    assert errors2[0]['name'] == 'name'
