from odm.field import Field
from odm.validations import is_required, is_email


def encrypt_password(value):
    return '$2a$' + value


class User(object):
    id = Field(
        default='abcd1234'
    )
    name = Field(
        validations=(is_required,)
    )
    email = Field(
        validations=(is_email,),
        access='private',
        default='test@example.com',
        unique=True,
    )
    password = Field(
        validations=(is_required,),
        access=False,
        before_save=encrypt_password
    )


user = User()


def test_init(app, db_conn):
    """
    Expect a field to initialize with default values.
    """
    assert isinstance(User.password.validations, tuple)
    assert user.password is None
    assert User.password.access is False
    assert User.password.before_save is encrypt_password
    assert User.email.default == 'test@example.com'
    assert User.password.unique is False
    assert User.email.unique is True


def test_get(app, db_conn):
    """
    Expect a field to get its value.
    """
    user.id = 'abcd1234'
    assert user.id == 'abcd1234'
    user.id = None


def test_get_default(app, db_conn):
    """
    Expect a field to default on get.
    """
    assert user.email == 'test@example.com'
    assert user.id == 'abcd1234'


def test_before_save(app, db_conn):
    """
    Expect a field to be able to use before_save when going into the database.
    """
    user.password = 'abcd1234'
    assert User.password.bundle(user) == '$2a$abcd1234'
    user.password = None


def test_access(app, db_conn):
    """
    Expect a field to check before providing as JSON.
    """
    user.password = 'abcd1234'
    assert User.password.deliver(user) is None
    user.password = None


def test_set(app, db_conn):
    """
    Expect a field to set its value.
    """
    assert user.name is None
    user.name = 'test'
    assert user.name == 'test'
    user.name = None


def test_validate(app, db_conn):
    """
    Expect a field to validate itself.
    """
    assert isinstance(User.name.validate(user), str)
    user.name = 'test'
    assert User.name.validate(user) is None
    user.name = None
