from foundations.model2 import Field, Model
from foundations.validations import required, email, minlength


class User(Model):
    tablename = 'users'
    name = Field(
        validations=(required),
        unique=True,
    )
    email = Field(
        validations=(required, email),
        unique=True,
    )
    password = Field(
        validations=(required, (minlength, 8)),
    )


def test_require(app, db_conn):
    """
    Expect a validation to require a field.
    """
    user = User({
        'name': 'test',
        'password': 'abcd1234'
    })
    assert required(user.name) is None
    assert required(user.email)


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
    assert email(user.email) is None
    assert email(user2.email)


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
    assert minlength(user.password, (8,)) is None
    assert minlength(user2.password, (8,))
