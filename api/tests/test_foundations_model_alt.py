from foundations.model_alt import Field, Model, embed, embed_many
from foundations.model_alt_validations import required, boolean, unique, \
    email, minlength
from modules.util import uniqid


def encrypt_password(str):
    return '$2a$' + str


class Settings(Model):
    receive_notifications = Field(
        validations=(boolean,),
        default=False,
    )


class User(Model):
    tablename = 'users'
    id = Field(
        validations=(required, unique),
        set=uniqid
    )
    name = Field(
        validations=(required, unique)
    )
    email = Field(
        validations=(required, unique, email),
        access='private'
    )
    password = Field(
        validations=(required, (minlength, 8)),
        access='hidden',
        set=encrypt_password
    )
    settings = embed(Settings)


class Book(Model):
    name = Field(validations=(required,))


class Author(User):
    book = embed_many(Book)


def test_table_class(app, db_conn):
    """
    Expect the model to have a table as a class.
    """
    assert False


def test_table_instance(app, db_conn):
    """
    Expect the model to have a table as an instance.
    """
    assert False


def test_get_id(app, db_conn):
    """
    Expect to be able to retrieve a model by ID.
    """
    assert False


def test_get_params(app, db_conn):
    """
    Expect a model to retrieve by params.
    """
    assert False


def test_get_none(app, db_conn):
    """
    Expect a no model when `get` with no match.
    """
    assert False


def test_list(app, db_conn):
    """
    Expect to get a list of models.
    """
    assert False


def test_list_params(app, db_conn):
    """
    Expect to get a list of models by params.
    """
    assert False


def test_list_none(app, db_conn):
    """
    Expect to get an empty list of models when none.
    """
    assert False


def test_insert(app, db_conn):
    """
    Expect to create a new model instace.
    """
    assert False


def test_insert_fail(app, db_conn):
    """
    Expect to error on failed create model.
    """
    assert False


def test_update(app, db_conn):
    """
    Expect to update a model instance.
    """
    assert False


def test_update_fail(app, db_conn):
    """
    Expect to error on failed update model instance.
    """
    assert False


def test_sync(app, db_conn):
    """
    Expect to sync fields with database.
    """
    assert False


def test_delete(app, db_conn):
    """
    Expect to delete a model.
    """
    assert False


def test_json(app, db_conn):
    """
    Expect to get JSON fields.
    """
    assert False


def test_id(app, db_conn):
    """
    Expect a model to have an ID.
    """
    assert False


def test_id_keep(app, db_conn):
    """
    Expect a model to maintain an ID.
    """
    assert False


def test_created(app, db_conn):
    """
    Expect a model to add created and modified.
    """
    assert False


def test_modified(app, db_conn):
    """
    Expect a model to update modified.
    """
    assert False


def test_ignore(app, db_conn):
    """
    Expect a model to ignore unschema'd fields.
    """
    assert False


def test_validate_success(app, db_conn):
    """
    Expect success on valid model.
    """
    assert False


def test_validate_fail(app, db_conn):
    """
    Expect errors on invalid model.
    """
    assert False


def test_require(app, db_conn):
    """
    Expect a model to require a field.
    """
    assert False


def test_unique(app, db_conn):
    """
    Expect a model to test uniqueness.
    """
    assert False


def test_email(app, db_conn):
    """
    Expect a model to validate email format.
    """
    assert False


def test_minlength(app, db_conn):
    """
    Expect a model to require a minimum length.
    """
    assert False


def test_embed(app, db_conn):
    """
    Expect a model to embed a document.
    """
    assert False


def test_embed_many(app, db_conn):
    """
    Expect a model to embed many documents.
    """
    assert False


def test_extend(app, db_conn):
    """
    Expect a model to be extendable.
    """
    assert False


def test_url(app, db_conn):
    """
    Expect a model to provide URLs.
    """
    assert False
