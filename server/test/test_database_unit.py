from datetime import datetime
from database.unit import insert_unit


def test_entity_id(db_conn, units_table):
    """
    Expect a unit to require an entity_id.
    """

    unit, errors = insert_unit(db_conn, {
        'user_id': 'abcd1234',
        'name': 'Learn this',
        'body': 'Learn how to do this',
    })
    assert len(errors) == 0
    unit['entity_id'] = 'JFKLD1234'
    unit, errors = insert_unit(db_conn, unit)
    assert len(errors) == 0


def test_previous(db_conn, units_table):
    """
    Expect a version previous_id to be a string or None.
    """

    unit, errors = insert_unit(db_conn, {
        'user_id': 'abcd1234',
        'name': 'Learn this',
        'body': 'Learn how to do this',
    })
    assert len(errors) == 0
    unit['previous_id'] = 'AFJkl345'
    unit, errors = insert_unit(db_conn, unit)
    assert len(errors) == 0


def test_language(db_conn, units_table):
    """
    Expect a unit to require a language.
    """

    unit, errors = insert_unit(db_conn, {
        'user_id': 'abcd1234',
        'name': 'Learn this',
        'body': 'Learn how to do this',
    })
    assert len(errors) == 0
    assert unit['language'] == 'en'


def test_name(db_conn, units_table):
    """
    Expect a unit to require a name.
    """

    unit, errors = insert_unit(db_conn, {
        'user_id': 'abcd1234',
        'body': 'Learn how to do this',
    })
    assert len(errors) == 1
    unit['name'] = 'Learn this'
    unit, errors = insert_unit(db_conn, unit)
    assert len(errors) == 0


def test_body(db_conn, units_table):
    """
    Expect a unit to require a body.
    """

    unit, errors = insert_unit(db_conn, {
        'user_id': 'abcd1234',
        'name': 'Learn this',
    })
    assert len(errors) == 1
    unit['body'] = 'Learn how to do this'
    unit, errors = insert_unit(db_conn, unit)
    assert len(errors) == 0


def test_status(db_conn, units_table):
    """
    Expect a unit status to be a string.
    """

    unit, errors = insert_unit(db_conn, {
        'user_id': 'abcd1234',
        'name': 'Learn this',
        'body': 'Learn how to do this',
    })
    assert len(errors) == 0
    assert unit['status'] == 'pending'
    unit['status'] = 'accepted'
    unit, errors = insert_unit(db_conn, unit)
    assert len(errors) == 0


def test_tags(db_conn, units_table):
    """
    Expect a unit to allow tags.
    """

    unit, errors = insert_unit(db_conn, {
        'user_id': 'abcd1234',
        'name': 'Learn this',
        'body': 'Learn how to do this',
    })
    assert len(errors) == 0
    unit['tags'] = ['A', 'B']
    unit, errors = insert_unit(db_conn, unit)
    assert len(errors) == 0


def test_requires(db_conn, units_table):
    """
    Expect a unit to allow requires ids.
    """

    units_table.insert({
        'user_id': 'abcd1234',
        'entity_id': 'A',
        'status': 'accepted',
        'created': datetime.utcnow(),
    }).run(db_conn)
    unit, errors = insert_unit(db_conn, {
        'user_id': 'abcd1234',
        'name': 'Learn this',
        'body': 'Learn how to do this',
    })
    assert len(errors) == 0
    unit['require_ids'] = ['A']
    unit, errors = insert_unit(db_conn, unit)
    assert len(errors) == 0
