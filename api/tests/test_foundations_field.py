from foundations.field import Field
from foundations.validations import required, email
import pytest


def encrypt_password(field):
    return '$2a$' + field.get()


def is_current_user(field):
    return True


def generate_id(field):
    return 'abcd1234'


id = Field(
    default=generate_id
)
name = Field(
    validations=(required,)
)
email = Field(
    validations=(email,),
    access=is_current_user,
    default='test@example.com',
    unique=True,
)
password = Field(
    validations=(required,),
    access=False,
    before_save=encrypt_password
)


def test_init(app, db_conn):
    """
    Expect a field to initialize with default values.
    """
    assert isinstance(password.validations, tuple)
    assert password.value is None
    assert password.access is False
    assert password.before_save is encrypt_password
    assert email.default == 'test@example.com'
    assert password.unique is False
    assert email.unique is True


def test_get(app, db_conn):
    """
    Expect a field to get its value.
    """
    id.value = 'abcd1234'
    assert id.get() == 'abcd1234'
    id.value = None


def test_get_default(app, db_conn):
    """
    Expect a field to default on get.
    """
    assert email.get() == 'test@example.com'
    assert id.get() == 'abcd1234'


def test_before_save(app, db_conn):
    """
    Expect a field to be able to use before_save when going into the database.
    """
    password.set('abcd1234')
    assert password.to_database() == '$2a$abcd1234'
    password.set(None)


def test_set(app, db_conn):
    """
    Expect a field to set its value.
    """
    assert name.get() is None
    name.set('test')
    assert name.get() == 'test'
    name.value = None


def test_validate(app, db_conn):
    """
    Expect a field to validate itself.
    """
    assert isinstance(name.validate(), basestring)
    name.set('test')
    assert name.validate() is None
    name.set(None)


@pytest.mark.xfail
def test_unique(app, db_conn, users_table):
    """
    Expect a validation to test uniqueness.
    """
    # user, errors = User.insert({
    #     'name': 'test',
    #     'email': 'test@example.com',
    #     'password': 'abcd1234'
    # })
    # user2 = User({
    #     'name': 'test'
    # })
    # assert unique(user, 'name') is None
    # assert unique(user2, 'name')
    assert False
