from odm.model import Field, Model, Document
from odm.validations import is_required, has_min_length
from odm.embed import Embeds, EmbedsMany
import pytest


class User(Model):
    tablename = 'users'
    name = Field(validations=(is_required,))


class Book(Document):
    name = Field(
        default='Untitled'
    )
    serial = Field(
        validations=(is_required,),
        unique=True,
        access=False,
    )


class Biography(Document):
    location = Field(
        default='Unknown',
        access=False
    )
    body = Field(
        validations=(is_required,),
    )


class Author(User):
    biography = Embeds(
        Biography,
        validations=(is_required,),
        access='private'
    )
    books = EmbedsMany(
        Book,
        validations=((has_min_length, 2),),
        access='private'
    )


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


def test_validation(app, db_conn):
    """
    Expect validation on embedded document.
    """
    author = Author({
        'name': 'Dalton',
        'books': [
            {'serial': 1234},
            {'serial': 5678}
        ]
    })
    errors = author.validate()
    assert len(errors) == 1
    assert errors[0]['name'] == 'biography'
    author.update_fields({
        'biography': {
            'body': 'Lorem ipsum.'
        }
    })
    errors = author.validate()
    assert len(errors) == 0


def test_validation_fields(app, db_conn):
    """
    Expect validation on embedded document fields.
    """
    author = Author({
        'name': 'Dalton',
        'biography': {
            'location': 'Arkansas'
        },
        'books': [
            {'serial': 1234},
            {'serial': 5678}
        ]
    })
    errors = author.validate()
    assert len(errors) == 1
    assert errors[0]['message'][0]['name'] == 'body'
    author.update_fields({
        'biography': {
            'body': 'Lorem ipsum.'
        }
    })
    errors = author.validate()
    assert len(errors) == 0


def test_validation_many(app, db_conn):
    """
    Expect validation on list of embedded documents.
    """
    author = Author({
        'name': 'Dalton',
        'biography': {
            'body': 'Lorem ipsum.'
        },
        'books': []
    })
    errors = author.validate()
    assert len(errors) == 1
    assert errors[0]['name'] == 'books'
    author.update_fields({
        'books': [
            {'serial': 1234},
            {'serial': 5678}
        ]
    })
    errors = author.validate()
    assert len(errors) == 0


def test_validation_many_fields(app, db_conn):
    """
    Expect validation on list of embedded document fields.
    """
    author = Author({
        'name': 'Dalton',
        'biography': {
            'body': 'Lorem ipsum.'
        },
        'books': [
            {'name': 'Red'},
            {'name': 'Blue'}
        ]
    })
    errors = author.validate()
    assert len(errors) == 1
    print errors
    assert errors[0]['message'][0]['name'] == 'serial'
    author.update_fields({'books': [
        {'serial': 1234},
        {'serial': 5678},
    ]})
    errors = author.validate()
    assert len(errors) == 0


def test_access(app, db_conn):
    """
    Expect access to trickle down to embedded document.
    """
    author = Author({
        'name': 'Dalton',
        'biography': {
            'body': 'Lorem ipsum.'
        },
        'books': [{
            'name': 'Red',
            'serial': 1234,
        }, {
            'name': 'Blue',
            'serial': 5678
        }]
    })
    assert not 'biography' in author.deliver()
    assert 'biography' in author.deliver(private=True)


def test_access_many(app, db_conn):
    """
    Expect access to trickle down to lists of embedded documents.
    """
    author = Author({
        'name': 'Dalton',
        'biography': {
            'body': 'Lorem ipsum.'
        },
        'books': [{
            'name': 'Red',
            'serial': 1234,
        }, {
            'name': 'Blue',
            'serial': 5678
        }]
    })
    assert not 'books' in author.deliver()
    assert 'books' in author.deliver(private=True)


def test_access_fields(app, db_conn):
    """
    Expect access to trickle down to embedded document fields.
    """
    author = Author({
        'name': 'Dalton',
        'biography': {
            'location': 'Dallas',
            'body': 'Lorem ipsum.'
        },
        'books': [{
            'name': 'Red',
            'serial': 1234,
        }, {
            'name': 'Blue',
            'serial': 5678
        }]
    })
    assert not 'location' in author.deliver(private=True)['biography']


def test_access_many_fields(app, db_conn):
    """
    Expect access to trickle down to lists of embedded document fields.
    """
    author = Author({
        'name': 'Dalton',
        'biography': {
            'body': 'Lorem ipsum.'
        },
        'books': [{
            'name': 'Red',
            'serial': 1234,
        }, {
            'name': 'Blue',
            'serial': 5678
        }]
    })
    assert not 'serial' in author.deliver(private=True)['books'][0]


def test_get_db(app, db_conn, users_table):
    """
    Expect to get a model with an embedded document from the database.
    """
    users_table.insert({
        'id': 'abcd1234',
        'name': 'Dalton',
        'biography': {
            'body': 'Lorem ipsum.'
        }
    }).run(db_conn)
    author = Author.get(id='abcd1234')
    assert author.name.get() == 'Dalton'
    assert author.biography.get().body.get() == 'Lorem ipsum.'


def test_get_db_many(app, db_conn, users_table):
    """
    Expect to get a model with a list of embedded document from the database.
    """
    users_table.insert({
        'id': 'abcd1234',
        'name': 'Dalton',
        'books': [{
            'name': 'Red',
            'serial': 1234,
        }, {
            'name': 'Blue',
            'serial': 5678
        }]
    }).run(db_conn)
    author = Author.get(id='abcd1234')
    assert author.name.get() == 'Dalton'
    assert author.books.get()[0].name.get() == 'Red'
    assert author.books.get()[1].serial.get() == 5678


def test_list_db(app, db_conn, users_table):
    """
    Expect to list models with embedded documents from the database.
    """
    users_table.insert([{
        'id': 'abcd1234',
        'biography': {
            'body': 'Lorem redsum.',
        }
    }, {
        'id': 'efgh5678',
        'biography': {
            'body': 'Lorem bluesum.',
        }
    }]).run(db_conn)
    authors = Author.list()
    assert 'Lorem redsum.' in [
        author.biography.get().body.get()
        for author in authors
    ]
    assert 'Lorem bluesum.' in [
        author.biography.get().body.get()
        for author in authors
    ]


def test_list_db_many(app, db_conn, users_table):
    """
    Expect to list models with lists of embedded documents from the database.
    """
    users_table.insert([{
        'id': 'abcd1234',
        'books': [{
            'name': 'Red',
        }, {
            'name': 'Blue',
        }]
    }, {
        'id': 'efgh5678',
        'books': [{
            'name': 'Green',
        }, {
            'name': 'Yellow',
        }]
    }]).run(db_conn)
    authors = Author.list()
    assert 'Red' in [
        book.name.get()
        for author in authors
        for book in author.books.get()
    ]


def test_insert_db(app, db_conn, users_table):
    """
    Expect to insert a model with an embedded document into the database.
    Expect to insert a model with a list of embedded document
    into the database.
    """
    author, errors = Author.insert({
        'name': 'Dalton',
        'biography': {
            'location': 'Dallas',
            'body': 'Lorem ipsum.'
        },
        'books': [{
            'name': 'Red',
            'serial': 1234,
        }, {
            'name': 'Blue',
            'serial': 5678
        }]
    })
    assert len(errors) == 0
    record = users_table.get(author.id.get()).run(db_conn)
    assert record['biography']['location'] == 'Dallas'
    assert record['books'][0]['name'] == 'Red'


def test_update(app, db_conn, users_table):
    """
    Expect to update a model with an embedded document into the database.
    Expect to update a model with a list of embedded document
    into the database.
    """
    author, errors = Author.insert({
        'name': 'Dalton',
        'biography': {
            'location': 'Dallas',
            'body': 'Lorem ipsum.'
        },
        'books': [{
            'name': 'Red',
            'serial': 1234,
        }, {
            'name': 'Blue',
            'serial': 5678
        }]
    })
    assert len(errors) == 0
    author.update({
        'biography': {
            'location': 'San Antonio'
        },
        'books': [{
            'name': 'Purple'
        }]
    })
    record = users_table.get(author.id.get()).run(db_conn)
    assert record['biography']['location'] == 'San Antonio'
    assert record['books'][0]['name'] == 'Purple'
    assert record['books'][0]['serial'] == 1234


def test_sync(app, db_conn, users_table):
    """
    Expect to synchronize an embedded document.
    Expect to synchronize a list of embedded documents.
    """
    author, errors = Author.insert({
        'name': 'Dalton',
        'biography': {
            'location': 'Dallas',
            'body': 'Lorem ipsum.'
        },
        'books': [{
            'name': 'Red',
            'serial': 1234,
        }, {
            'name': 'Blue',
            'serial': 5678
        }]
    })
    assert author.id.get()


def test_delete(app, db_conn, users_table):
    """
    Expect to delete a model with an embedded document from the database.
    Expect to delete a model with a list of embedded document
    from the database.
    """
    author, errors = Author.insert({
        'name': 'Dalton',
        'biography': {
            'location': 'Dallas',
            'body': 'Lorem ipsum.'
        },
        'books': [{
            'name': 'Red',
            'serial': 1234,
        }, {
            'name': 'Blue',
            'serial': 5678
        }]
    })
    author.delete()
    records = users_table.run(db_conn)
    assert len(list(records)) == 0


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
