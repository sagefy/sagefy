from odm.model import Field, Document, Model
from odm.embed import has, has_many
from odm.validations import required, boolean, email, minlength
import pytest


def encrypt_password(field):
    return '$2a$' + field.get()


class Settings(Document):
    email_notifications = Field(
        validations=(boolean,),
        default=False,
    )


def is_current_user():
    return True


class User(Model):
    tablename = 'users'
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
    settings = has(Settings)

    def is_current_user(self):
        return is_current_user()


class Book(Document):
    name = Field(
        validations=(required,),
        default='Untitled'
    )


class Author(User):
    book = has_many(Book)


@pytest.mark.xfail
def test_extend(app, db_conn, users_table):
    """
    Expect a model to be extendable.
    """
    author = Author.insert({
        'name': 'test',
        'email': 'test@example.com',
        'password': 'abcd1234',
    })
    assert isinstance(author, User)
    assert isinstance(author, Author)
    assert author.name.get() == 'test'


@pytest.mark.xfail
def test_embed_many(app, db_conn, users_table):
    """
    Expect a model to embed many documents.
    """
    author = Author.insert({
        'name': 'test',
        'email': 'test@example.com',
        'password': 'abcd1234',
        'books': [
            {
                'name': 'sunrise'
            },
            {
                'name': 'sunset'
            }
        ]
    })
    assert author.books.get(0).name.get() == 'sunrise'
    assert author.books.get(1).name.get() == 'sunset'


@pytest.mark.xfail
def test_embed(app, db_conn, users_table):
    """
    Expect a model to embed a document.
    """
    user = User.insert({
        'name': 'test',
        'email': 'test@example.com',
        'password': 'abcd1234',
        'settings': {
            'email_notifications': True
        }
    })
    assert user.settings.email_notifications is True
