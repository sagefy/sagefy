from odm.model import Field, Document
from odm.validations import is_required, is_email, has_min_length


class User(Document):
    name = Field(
        validations=(is_required),
        unique=True,
    )
    email = Field(
        validations=(is_required, is_email),
        unique=True,
    )
    password = Field(
        validations=(is_required, (has_min_length, 8)),
    )


def test_require(app, db_conn):
    """
    Expect a validation to require a field.
    """
    user = User({
        'name': 'test',
        'password': 'abcd1234'
    })
    assert is_required(user.name) is None
    assert is_required(user.email)


def test_email(app, db_conn):
    """
    Expect a validation to validate email format.
    """
    user = User({
        'email': 'test@example.com',
    })
    user2 = User({
        'email': 'other'
    })
    assert is_email(user.email) is None
    assert is_email(user2.email)


def test_minlength(app, db_conn):
    """
    Expect a validation to require a minimum length.
    """
    user = User({
        'password': 'abcd1234'
    })
    user2 = User({
        'password2': 'a'
    })
    assert has_min_length(user.password, (8,)) is None
    assert has_min_length(user2.password, (8,))
