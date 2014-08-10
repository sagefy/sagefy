from foundations.model2 import Field, Document, Model
from foundations.embed import has, has_many, EmbeddedDocument, \
    ManyEmbeddedDocument
from foundations.validations import required, unique, boolean, email, minlength
from datetime import datetime


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
        validations=(required, unique)
    )
    email = Field(
        validations=(required, unique, email),
        access=is_current_user
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


def test_table_class(app, db_conn, users_table):
    """
    Expect the model to have a table as a class.
    """
    assert User.tablename == 'users'
    assert User.get_table() == users_table


def test_table_instance(app, db_conn, users_table):
    """
    Expect the model to have a table as an instance.
    """
    user = User()
    assert user.tablename == 'users'
    assert user.table == users_table


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


def test_get_id(app, db_conn, users_table):
    """
    Expect to be able to retrieve a model by ID.
    """
    users_table.insert({
        'id': 'abcdefgh12345678',
        'name': 'test',
        'email': 'test@example.com',
    }).run(db_conn)
    user = User.get(id='abcdefgh12345678')
    assert user.name.get() == 'test'


def test_get_params(app, db_conn, users_table):
    """
    Expect a model to retrieve by params.
    """
    users_table.insert({
        'id': 'abcdefgh12345678',
        'name': 'test',
        'email': 'test@example.com',
    }).run(db_conn)
    user = User.get(name='test', email='test@example.com')
    assert user.id.get() == 'abcdefgh12345678'


def test_get_none(app, db_conn, users_table):
    """
    Expect a no model when `get` with no match.
    """
    users_table.insert({
        'id': 'abcdefgh12345678',
        'name': 'test',
        'email': 'test@example.com',
    }).run(db_conn)
    user = User.get(id='87654321hgfedcba')
    assert user is None


def test_list(app, db_conn, users_table):
    """
    Expect to get a list of models.
    """
    users_table.insert([
        {
            'id': '1',
            'name': 'test1',
            'email': 'test1@example.com',
        },
        {
            'id': '2',
            'name': 'test2',
            'email': 'test2@example.com',
        },
        {
            'id': '3',
            'name': 'test3',
            'email': 'test3@example.com',
        },
    ]).run(db_conn)
    users = User.list()
    assert len(users) == 3
    assert isinstance(users[0], User)
    assert users[2].id.get() in ('1', '2', '3')


def test_list_params(app, db_conn, users_table):
    """
    Expect to get a list of models by params.
    """
    users_table.insert([
        {
            'id': '1',
            'name': 'test1',
            'email': 'test1@example.com',
        },
        {
            'id': '2',
            'name': 'test2',
            'email': 'test2@example.com',
        },
        {
            'id': '3',
            'name': 'test3',
            'email': 'test3@example.com',
        },
    ]).run(db_conn)
    users = User.list(id='1', name='test1')
    assert len(users) == 1
    assert users[0].email.get() == 'test1@example.com'


def test_list_none(app, db_conn, users_table):
    """
    Expect to get an empty list of models when none.
    """
    users = User.list()
    assert len(users) == 0


def test_get_fields(app, db_conn):
    """
    Expect to get able to get the fields on a Model.
    """
    user = User()
    for name, field in user.get_fields():
        assert isinstance(name, basestring)
        assert isinstance(field, (Field, EmbeddedDocument,
                                  ManyEmbeddedDocument))


def test_generate_id(app, db_conn, users_table):
    """
    Expect to automatically generate an ID.
    """
    user = User()
    d = user.to_database()
    assert isinstance(d['id'], basestring)
    assert len(d['id']) == 16


def test_insert(app, db_conn, users_table):
    """
    Expect to create a new model instance.
    """
    user, errors = User.insert({
        'name': 'test',
        'email': 'test@example.com',
        'password': 'abcd1234'
    })
    assert len(errors) == 0
    record = list(users_table.filter({'name': 'test'}).run(db_conn))[0]
    assert user.id.get()
    assert user.name.get() == 'test'
    assert record['email'] == 'test@example.com'


def test_insert_fail(app, db_conn, users_table):
    """
    Expect to error on failed create model.
    """
    assert len(list(users_table.run(db_conn))) == 0
    user, errors = User.insert({
        'email': 'test@example.com'
    })
    assert user.name.get() is None
    assert user.password.get() is None
    assert isinstance(user, User)
    assert isinstance(errors, (list, tuple))
    assert len(errors) == 2
    assert errors[0]['message']


def test_update(app, db_conn, users_table):
    """
    Expect to update a model instance.
    """
    user, errors = User.insert({
        'name': 'test',
        'email': 'test@example.com',
        'password': 'abcd1234'
    })
    assert len(errors) == 0
    user, errors = user.update({
        'email': 'open@example.com'
    })
    assert len(errors) == 0
    record = list(users_table.filter({'name': 'test'}).run(db_conn))[0]
    assert user.email.get() == 'open@example.com'
    assert record['email'] == 'open@example.com'


def test_update_fail(app, db_conn, users_table):
    """
    Expect to error on failed update model instance.
    """
    user, errors = User.insert({
        'name': 'test',
        'email': 'test@example.com',
        'password': 'abcd1234'
    })
    assert len(errors) == 0
    user, errors = user.update({
        'email': 'open'
    })
    record = list(users_table.filter({'name': 'test'}).run(db_conn))[0]
    assert isinstance(user, User)
    assert isinstance(errors, (list, tuple))
    assert user.email.get() == 'open'
    assert record['email'] == 'test@example.com'


def test_delete(app, db_conn, users_table):
    """
    Expect to delete a model.
    """
    user, errors = User.insert({
        'name': 'test',
        'email': 'test@example.com',
        'password': 'abcd1234'
    })
    assert len(errors) == 0
    user.delete()
    records = list(users_table.filter({'name': 'test'}).run(db_conn))
    assert len(records) == 0


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


def test_access(app, db_conn):
    """
    Expect a model to only give fields matching access.
    """
    user = User({
        'name': 'test',
        'email': 'test@example.com',
        'password': 'abcd1234'
    })
    fields = user.to_json()
    assert 'email' in fields
    assert 'password' not in fields


def test_id_keep(app, db_conn, users_table):
    """
    Expect a model to maintain an ID.
    """
    user, errors = User.insert({
        'name': 'test',
        'email': 'test@example.com',
        'password': 'abcd1234'
    })
    id = user.id.get()
    user.update({
        'name': 'other'
    })
    assert user.id.get() == id


def test_created(app, db_conn, users_table):
    """
    Expect a model to add created time.
    """
    user, errors = User.insert({
        'name': 'test',
        'email': 'test@example.com',
        'password': 'abcd1234'
    })
    record = list(users_table.filter({'name': 'test'}).run(db_conn))[0]
    assert record['created'] == user.created.get()


def test_modified(app, db_conn, users_table):
    """
    Expect to sync fields with database.
    """
    user, errors = User.insert({
        'name': 'test',
        'email': 'test@example.com',
        'password': 'abcd1234'
    })
    user, errors = user.update({
        'email': 'other@example.com'
    })
    record = list(users_table.filter({'name': 'test'}).run(db_conn))[0]
    assert isinstance(user.modified.get(), datetime)
    assert record['modified'] == user.modified.get()
    assert user.created.get() != user.modified.get()


def test_not_field(app, db_conn, users_table):
    """
    Expect a model to error on unschema'd fields.
    """
    user, errors = User.insert({
        'name': 'test',
        'email': 'test@example.com',
        'password': 'abcd1234',
        'color': 'blue',
    })
    assert isinstance(user, User)
    assert len(errors) > 1


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


def test_url(app, db_conn, users_table):
    """
    Expect a model to provide URLs.
    """
    user = User.insert({
        'name': 'test',
        'email': 'test@example.com',
        'password': 'abcd1234'
    })
    assert user.get_url().startswith('/users/')


def test_require(app, db_conn):
    """
    Expect a validation to require a field.
    """
    user = User({
        'name': 'test',
        'password': 'abcd1234'
    })
    assert required(user, 'name') is None
    assert required(user, 'email')['message']


def test_unique(app, db_conn, users_table):
    """
    Expect a validation to test uniqueness.
    """
    user = User.insert({
        'name': 'test',
        'email': 'test@example.com',
        'password': 'abcd1234'
    })
    user2 = User({
        'name': 'test'
    })
    assert unique(user, 'name') is None
    assert unique(user2, 'name')['message']


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
    assert email(user, 'email') is None
    assert email(user2, 'email')['message']


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
    assert minlength(user, 'password', 8) is None
    assert minlength(user2, 'password', 8)['message']


def test_default(app, db_conn):
    """
    Expect a field to set default values.
    """
    user = User({
        'settings': {}
    })
    assert user.settings.get().email_notifications.get() is False


def test_before_save(app, db_conn, users_table):
    """
    Expect a model to call before_save before going into DB.
    """
    user = User.insert({
        'name': 'test',
        'email': 'test@example.com',
        'password': 'abcd1234'
    })
    assert user.password.get().startswith('$2a$')
