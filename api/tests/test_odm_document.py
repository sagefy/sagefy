from odm.field import Field
from odm.document import Document
from odm.validations import required, email, minlength


def encrypt_password(field):
    return '$2a$' + field.get()


def is_current_user(field):
    return True


class User(Document):
    name = Field(
        validations=(required,),
        unique=True
    )
    email = Field(
        validations=(required, email),
        access='private',
        unique=True
    )
    password = Field(
        validations=(required, (minlength, 8)),
        access=False,
        before_save=encrypt_password
    )

    def is_current_user(self):
        return is_current_user()


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
    assert user.name.get() == 'test'


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
    for name, field in user.get_fields():
        assert isinstance(name, basestring)
        assert isinstance(field, Field)


def test_create_instance(app, db_conn):
    """
    Expect to create a model, no DB, on dict of fields.
    """
    user = User({'name': 'test'})
    assert user.name.get() == 'test'


def test_create_instance_other(app, db_conn):
    """
    Expect to create a model, no DB, setting properties.
    """
    user = User()
    user.name.set('test')
    assert user.name.get() == 'test'


def test_to_database(app, db_conn):
    """
    Expect to database to get database ready
    versions of all fields
    """
    User.password.set('abcd1234')
    assert User.password.to_database() == '$2a$abcd1234'
    User.password.set(None)


def test_json(app, db_conn):
    """
    Expect to get JSON fields.
    """
    user = User({
        'name': 'test',
        'email': 'test@example.com',
        'password': 'abcd1234'
    })
    fields = user.to_json()
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
    fields = user.to_json(private=True)
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
