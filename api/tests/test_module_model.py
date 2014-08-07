from modules.model import Model
from app import make_db_connection, close_db_connection


class TestModel(Model):
    tablename = 'tests'


def test_model_table(app):
    # Ensure we can grab the model's table
    make_db_connection(app)
    assert TestModel.get_table()
    close_db_connection(None)


def test_create_instance(app):
    # Expect the class to be able to make an instance with fields
    make_db_connection(app)
    fields = {'a': 1}
    x = TestModel(fields)
    assert x.table
    assert x.fields['a'] == 1
    close_db_connection(None)
