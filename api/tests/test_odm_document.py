from odm.field import Field
from odm.document import Document
from odm.validations import is_required, is_email, has_min_length


def encrypt_password(value):
    return '$2a$' + value


class User(Document):
    name = Field(
        validations=(is_required,),
        unique=True
    )
    email = Field(
        validations=(is_required, is_email),
        access='private',
        unique=True
    )
    password = Field(
        validations=(is_required, (has_min_length, 8)),
        access=False,
        before_save=encrypt_password
    )


def test_isfield(app, db_conn):
    """
    Expect to test if an instance is a field.
    """
    assert User.isfield(User.name)
    assert not User.isfield(True)


def test_get_fields(app, db_conn):
    """
    Expect to get able to get the fields on a Model.
    """
    user = User()
    fields = user.get_fields()
    names = [name for name, field in fields]
    assert 'name' in names
    assert 'email' in names
    assert 'password' in names
    for name, field in fields:
        assert isinstance(name, basestring)
        assert isinstance(field, Field)


def test_init_fields(app, db_conn):
    """
    Expect fields to be a duplicate per instance.
    """
    user = User()
    assert user.name is not User.name


def test_update_fields(app, db_conn):
    """
    Expect a document to update the fields.
    """
    user = User()
    user.update_fields({
        'name': 'test'
    })
    assert user.name == 'test'


def test_not_field(app, db_conn):
    """
    Expect a model to error on unschema'd fields.
    """
    user = User()
    user, errors = user.update_fields({
        'name': 'test',
        'email': 'test@example.com',
        'password': 'abcd1234',
        'color': 'blue',
    })
    assert isinstance(user, User)
    assert len(errors) == 1
    assert errors[0]['name'] == 'color'


def test_create_instance(app, db_conn):
    """
    Expect to create a model, no DB, on dict of fields.
    """
    user = User({'name': 'test'})
    assert user.name == 'test'


def test_create_instance_other(app, db_conn):
    """
    Expect to create a model, no DB, setting properties.
    """
    user = User()
    user.name = 'test'
    assert user.name == 'test'


def test_bundle(app, db_conn):
    """
    Expect to database to get database ready
    versions of all fields
    """
    user = User()
    user.password = 'abcd1234'
    assert user.bundle()['password'] == '$2a$abcd1234'
    user.password = None


def test_json(app, db_conn):
    """
    Expect to get JSON fields.
    """
    user = User({
        'name': 'test',
        'email': 'test@example.com',
        'password': 'abcd1234'
    })
    fields = user.deliver()
    assert isinstance(fields, dict)
    assert fields['name'] == 'test'


def test_json_access(app, db_conn):
    """
    Expect a model to only give fields matching access.
    """
    user = User({
        'name': 'test',
        'email': 'test@example.com',
        'password': 'abcd1234'
    })
    fields = user.deliver(private=True)
    assert 'email' in fields
    assert 'password' not in fields


def test_validate_success(app, db_conn):
    """
    Expect success on valid model.
    """
    user = User({
        'name': 'test',
        'email': 'test@example.com',
        'password': 'abcd1234',
    })
    errors = user.validate()
    assert len(errors) == 0


def test_validate_fail(app, db_conn):
    """
    Expect errors on invalid model.
    """
    user = User({
        'name': 'test',
        'email': 'test@example.com',
    })
    errors = user.validate()
    assert len(errors) == 1
