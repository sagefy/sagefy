from odm.model import Field, Model, Document
from odm.validations import required, email, minlength
from odm.embed import Has, HasMany
import pytest


def encrypt_password(field):
    return '$2a$' + field.get()


class User(Model):
    tablename = 'users'
    name = Field(
        validations=(required,),
        unique=True,
    )
    email = Field(
        validations=(required, email),
        unique=True,
        access='private'
    )
    password = Field(
        validations=(required, (minlength, 8)),
        access=False,
        before_save=encrypt_password
    )

    def is_current_user(self):
        return True


class Book(Document):
    name = Field(
        validations=(required,),
        default='Untitled'
    )
    serial = Field(
        validations=(required,),
        unique=True
    )


class Biography(Document):
    location = Field(
        default='Unknown',
    )
    body = Field(
        validations=(required,),
    )


class Author(User):
    biography = Has(Biography)
    books = HasMany(Book)


def test_embed(app, db_conn):
    """
    Expect to embed a document on a model.
    """
    author = Author()
    assert author.biography
    assert Author.biography.Doc == Biography


def test_embed_many(app, db_conn):
    """
    Expect to embed a list of documents on a model.
    """
    author = Author()
    assert author.books
    assert isinstance(author.books.value, list)
    assert Author.books.Doc == Book


def test_embed_set(app, db_conn):
    """
    Expect to set fields on embedded document.
    """
    author = Author()
    author, errors = author.update_fields({
        'biography': {
            'body': 'Lorem ipsum.'
        }
    })
    assert author.biography.value.body.value == 'Lorem ipsum.'
    assert len(errors) == 0


def test_embed_many_set(app, db_conn):
    """
    Expect to set fields on list embedded document.
    """
    author = Author()
    author, errors = author.update_fields({
        'books': [{
            'name': 'Red',
            'serial': 123,
        }, {
            'name': 'Blue',
            'serial': 456
        }]
    })
    assert author.books.value[0].name.value == 'Red'
    assert author.books.value[1].serial.value == 456
    assert len(errors) == 0


def test_embed_get(app, db_conn):
    """
    Expect to get a document embedded.
    """
    author = Author({
        'biography': {
            'body': 'Lorem ipsum.'
        }
    })
    assert author.biography.get().body.get() == 'Lorem ipsum.'


def test_embed_many_get(app, db_conn):
    """
    Expect to get a list of documents embedded.
    """
    author = Author({
        'books': [{
            'name': 'Red',
            'serial': 123,
        }, {
            'name': 'Blue',
            'serial': 456
        }]
    })
    assert author.books.get()[0].name.get() == 'Red'
    assert author.books.get()[1].serial.get() == 456


def test_embed_default(app, db_conn):
    """
    Expect to get defaults on embedded documents.
    """
    author = Author({
        'biography': {}
    })
    assert author.biography.get().location.get() == 'Unknown'


def test_embed_many_default(app, db_conn,):
    """
    Expect to get defaults on lists of embedded documents.
    """
    author = Author({
        'books': [{
            'serial': 123
        }]
    })
    assert author.books.get()[0].name.get() == 'Untitled'


def test_embed_update(app, db_conn):
    """
    Expect to update fields on embedded document.
    """
    author = Author({
        'biography': {
            'body': 'Lorem ipsum.'
        }
    })
    assert author.biography.get().body.get() == 'Lorem ipsum.'
    author.update_fields({
        'biography': {
            'body': 'Ipsum lorem.'
        }
    })
    assert author.biography.get().body.get() == 'Ipsum lorem.'
    author.biography.get().update_fields({
        'body': 'Lorem ipsyum.'
    })
    assert author.biography.get().body.get() == 'Lorem ipsyum.'


def test_embed_many_update(app, db_conn):
    """
    Expect to update fields on list embedded document.
    """
    author = Author({
        'books': [{
            'name': 'Red',
            'serial': 123,
        }, {
            'name': 'Blue',
            'serial': 456
        }]
    })
    assert author.books.get()[0].name.get() == 'Red'
    assert author.books.get()[1].serial.get() == 456
    author.books.get()[0].update_fields({
        'name': 'Yellow'
    })
    assert author.books.get()[0].name.get() == 'Yellow'


def test_embed_append(app, db_conn):
    """
    Expect to add a new embedded document to list.
    """
    author = Author({
        'books': [{
            'name': 'Red',
            'serial': 123,
        }]
    })
    assert len(author.books.get()) == 1
    author.books.get().append(Book({
        'name': 'Blue',
        'serial': 456
    }))
    assert len(author.books.get()) == 2
    assert author.books.get()[1].name.get() == 'Blue'


def test_embed_splice(app, db_conn):
    """
    Expect to remove an embedded document from a list.
    """
    author = Author({
        'books': [{
            'name': 'Red',
            'serial': 123,
        }, {
            'name': 'Blue',
            'serial': 456
        }, {
            'name': 'Green',
            'serial': 789
        }]
    })
    assert len(author.books.get()) == 3
    author.books.get().pop(1)
    assert len(author.books.get()) == 2
    assert author.books.get()[0].name.get() == 'Red'
    assert author.books.get()[1].name.get() == 'Green'


@pytest.mark.xfail
def test_embed_before(app, db_conn):
    """
    Expect before_save called on embedded document.
    """
    assert False


@pytest.mark.xfail
def test_embed_fields_before(app, db_conn):
    """
    Expect before_save called on embedded document fields.
    """
    assert False


@pytest.mark.xfail
def test_embed_many_before(app, db_conn):
    """
    Expect before_save called on list of embedded documents.
    """
    assert False


@pytest.mark.xfail
def test_embed_many_fields_before(app, db_conn):
    """
    Expect before_save called on list of embedded documents fields.
    """
    assert False


@pytest.mark.xfail
def test_access(app, db_conn):
    """
    Expect access to trickle down to embedded document.
    """
    assert False


@pytest.mark.xfail
def test_access_fields(app, db_conn):
    """
    Expect access to trickle down to embedded document fields.
    """
    assert False


@pytest.mark.xfail
def test_access_many(app, db_conn):
    """
    Expect access to trickle down to lists of embedded documents.
    """
    assert False


@pytest.mark.xfail
def test_access_many_fields(app, db_conn):
    """
    Expect access to trickle down to lists of embedded document fields.
    """
    assert False


@pytest.mark.xfail
def test_validation(app, db_conn):
    """
    Expect validation on embedded document.
    """
    assert False


@pytest.mark.xfail
def test_validation_fields(app, db_conn):
    """
    Expect validation on embedded document fields.
    """
    assert False


@pytest.mark.xfail
def test_validation_many(app, db_conn):
    """
    Expect validation on list of embedded documents.
    """
    assert False


@pytest.mark.xfail
def test_validation_many_fields(app, db_conn):
    """
    Expect validation on list of embedded document fields.
    """
    assert False


@pytest.mark.xfail
def test_id(app, db_conn, users_table):
    """
    Expect only one ID for an entire model.
    """
    assert False


@pytest.mark.xfail
def test_created(app, db_conn, users_table):
    """
    Expect only one created time for an entire model.
    """
    assert False


@pytest.mark.xfail
def test_modified(app, db_conn, users_table):
    """
    Expect only one modified time for an entire model.
    """
    assert False


@pytest.mark.xfail
def test_sync(app, db_conn, users_table):
    """
    Expect to synchronize an embedded document.
    """
    assert False


@pytest.mark.xfail
def test_sync_many(app, db_conn, users_table):
    """
    Expect to synchronize a list of embedded documents.
    """
    assert False


@pytest.mark.xfail
def test_get_db(app, db_conn, users_table):
    """
    Expect to get a model with an embedded document from the database.
    """
    assert False


@pytest.mark.xfail
def test_get_db_many(app, db_conn, users_table):
    """
    Expect to get a model with a list of embedded document from the database.
    """
    assert False


@pytest.mark.xfail
def test_list_db(app, db_conn, users_table):
    """
    Expect to list models with embedded documents from the database.
    """
    assert False


@pytest.mark.xfail
def test_list_db_many(app, db_conn, users_table):
    """
    Expect to list models with lists of embedded documents from the database.
    """
    assert False


@pytest.mark.xfail
def test_insert_db(app, db_conn, users_table):
    """
    Expect to insert a model with an embedded document into the database.
    """
    assert False


@pytest.mark.xfail
def test_insert_db_many(app, db_conn, users_table):
    """
    Expect to insert a model with a list of embedded document
    into the database.
    """
    assert False


@pytest.mark.xfail
def test_update(app, db_conn, users_table):
    """
    Expect to update a model with an embedded document into the database.
    """
    assert False


@pytest.mark.xfail
def test_update_many(app, db_conn, users_table):
    """
    Expect to update a model with a list of embedded document
    into the database.
    """
    assert False


@pytest.mark.xfail
def test_delete(app, db_conn, users_table):
    """
    Expect to delete a model with an embedded document from the database.
    """
    assert False


@pytest.mark.xfail
def test_delete_many(app, db_conn, users_table):
    """
    Expect to delete a model with a list of embedded document
    from the database.
    """
    assert False


@pytest.mark.xfail
def test_unique(app, db_conn, users_table):
    """
    Expect unique to check embedded document fields.
    """
    assert False


@pytest.mark.xfail
def test_unique_many(app, db_conn, users_table):
    """
    Expect unique to check list embedded document fields.
    """
    assert False
