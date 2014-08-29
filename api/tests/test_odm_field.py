from odm.field import Field
from odm.validations import is_required, is_email


def encrypt_password(value):
    return '$2a$' + value


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
    assert password.bundle() == '$2a$abcd1234'
    password.set(None)


def test_access(app, db_conn):
    """
    Expect a field to check before providing as JSON.
    """
    password.set('abcd1234')
    assert password.deliver() is None
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
