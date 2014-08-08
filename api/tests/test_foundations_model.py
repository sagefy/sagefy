from foundations.model import Model


class TestModel(Model):
    tablename = 'tests'

    schema = {
        'a': {
            'validations': ('required',)
        },
    }


def test_model_table(app, db_conn):
    """
    Ensure we can grab the model's table.
    """
    assert TestModel.get_table()


def test_create_instance(app, db_conn):
    """
    Expect the class to be able to make an instance with fields.
    """
    fields = {'a': 1}
    x = TestModel(fields)
    assert x.table
    assert x.fields['a'] == 1


def test_get_model(app, db_conn, tests_table):
    """
    Ensure we can get a model, given an ID.
    """
    tests_table.insert({'id': 18, 'a': 27}).run(db_conn)
    x = TestModel.get(id=18)
    assert x.fields['a'] == 27


def test_get_model_param(app, db_conn, tests_table):
    """
    Ensure we can get a model, given an email.
    """
    tests_table.insert({'id': 18, 'a': 92}).run(db_conn)
    x = TestModel.get(a=92)
    assert x.fields['a'] == 92


def test_get_model_none(app, db_conn, tests_table):
    """
    If we call get, but no model matches, expect it to give us None.
    """
    x = TestModel.get(id=99)
    assert x is None


def test_list_model(app, db_conn, tests_table):
    """
    Expect list to give us an array of models.
    """
    tests_table.insert([
        {'id': 1, 'a': 10},
        {'id': 2, 'a': 15},
        {'id': 3, 'a': 10}
    ]).run(db_conn)
    models = TestModel.list(a=10)
    ids = [models[0].fields['id'], models[1].fields['id']]
    assert ids == [1, 3] or ids == [3, 1]


def test_list_empty(app, db_conn, tests_table):
    """
    Expect list to return empty if no models match parameters.
    """
    models = TestModel.list(a=10)
    assert models == []


def test_insert_model(app, db_conn, tests_table):
    """
    Expect insert to store a model.
    """
    fields = {'a': 10}
    model = TestModel(fields)
    valid, errors = model.insert()
    assert valid
    assert model.fields['a'] == 10
    assert len(list(tests_table.filter({'a': 10}).run(db_conn))) == 1


def test_insert_fail(app, db_conn, tests_table):
    """
    Expect insert to give False and errors if validation fails.
    """
    model = TestModel({})
    valid, errors = model.insert()
    assert not valid
    assert isinstance(errors, list)


def test_update_model(app, db_conn, tests_table):
    """
    Expect update to update a given model, given fields.
    """
    model = TestModel({'a': 10})
    model.insert()
    model.update({'a': 11})
    assert model.fields['a'] == 11
    assert len(list(tests_table.filter({'a': 11}).run(db_conn))) == 1


def test_fail_update_model(app, db_conn, tests_table):
    """
    Expect update to give validation errors.
    """
    model = TestModel({'a': 10})
    model.insert()
    valid, errors = model.update({'a': None})
    assert not valid
    assert isinstance(errors, list)


def test_sync_fields(app, db_conn, tests_table):
    """
    Expect sync to update the fields to the latest.
    """
    model = TestModel({'a': 10})
    model.insert()
    mod1 = model.fields['modified']
    model.update({'a': 11})
    mod2 = model.fields['modified']
    assert mod1 != mod2


def test_delete_model(app, db_conn, tests_table):
    """
    Expect delete to remove the model from the database.
    """
    model = TestModel({'a': 10})
    model.insert()
    model.delete()
    assert len(list(tests_table.run(db_conn))) == 0


def test_get_model_fields(app, db_conn):
    """
    Expect get fields to return the model's fields.
    """
    model = TestModel({'a': 10})
    assert model.get_fields()['a'] == 10


def test_model_tidy_id(app, db_conn):
    """
    Expect tidy fields to add an ID.
    """
    model = TestModel({'a': 10})
    model.tidy_fields()
    assert model.fields['id']


def test_tidy_keep_id(app, db_conn):
    """
    Expect tidy fields to maintain an existing ID.
    """
    assert False


def test_tidy_modified_time(app, db_conn):
    """
    Expect tidy fields to update the modified time.
    """
    assert False


def test_tidy_non_schema(app, db_conn):
    """
    Expect tidy fields to remove non schema'd keys.
    """
    assert False


def test_tidy_keep_schemad(app, db_conn):
    """
    Expect tidy fields to keep schema'd keys.
    """
    assert False


def test_tidy_encrypt_password(app, db_conn):
    """
    Expect tidy fields to encrypt a plain password.
    """
    assert False


def test_validate_schema(app, db_conn):
    """
    Expect validate to validate all fields in a schema.
    """
    assert False


def test_validate_success(app, db_conn):
    """
    Expect validate to be true when all fields valid.
    """
    assert False


def test_validate_error(app, db_conn):
    """
    Expect validate to give errors when fields don't match schema.
    """
    assert False


def test_validate_field(app, db_conn):
    """
    Expect validate field to run all validations on fields.
    """
    assert False


def test_validate_field_no_params(app, db_conn):
    """
    Expect validate field to work on a field with no parameters.
    """
    assert False


def test_validate_field_params(app, db_conn):
    """
    Expect validate field to work on a field with parameters.
    """
    assert False


def test_validate_field_error(app, db_conn):
    """
    Expect validate field to give error.
    """
    assert False


def test_validate_field_success(app, db_conn):
    """
    Expect validate field to give None when okay.
    """
    assert False


def test_validate_requied(app, db_conn):
    """
    Expect required to require the field.
    """
    assert False


def test_validate_unique(app, db_conn):
    """
    Expect unique to validate field uniqueness.
    """
    assert False


def test_validate_email(app, db_conn):
    """
    Expect email to ensure field is formatted as email.
    """
    assert False


def test_validate_minlength(app, db_conn):
    """
    Expect minlength to ensure field matches a minimum length.
    """
    assert False
