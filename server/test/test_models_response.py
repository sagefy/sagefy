from models.response import Response
import rethinkdb as r


def test_created(db_conn, responses_table):
    """
    Expect to have a created date.
    """

    response = Response({
        'user_id': 'A',
        'card_id': 'BC',
        'unit_id': 'RM',
        'response': 42,
        'score': 0.9,
        'learned': 0.9,
    })
    del response['created']  # should be set to default anywho
    response, errors = response.save(db_conn)
    assert len(errors) == 0


def test_user(db_conn, responses_table):
    """
    Expect to require a user ID.
    """

    response, errors = Response.insert(db_conn, {
        'card_id': 'BC',
        'unit_id': 'RM',
        'response': 42,
        'score': 0.9,
        'learned': 0.9,
    })
    assert len(errors) == 1
    response['user_id'] = 'A'
    response, errors = response.save(db_conn)
    assert len(errors) == 0


def test_card(db_conn, responses_table):
    """
    Expect to require a card ID.
    """

    response, errors = Response.insert(db_conn, {
        'user_id': 'A',
        'unit_id': 'RM',
        'response': 42,
        'score': 0.9,
        'learned': 0.9,
    })
    assert len(errors) == 1
    response['card_id'] = 'AFJ'
    response, errors = response.save(db_conn)
    assert len(errors) == 0


def test_unit(db_conn, responses_table):
    """
    Expect to require a unit ID.
    """

    response, errors = Response.insert(db_conn, {
        'user_id': 'A',
        'card_id': 'BC',
        'response': 42,
        'score': 0.9,
        'learned': 0.9,
    })
    assert len(errors) == 1
    response['unit_id'] = 'A24JLD'
    response, errors = response.save(db_conn)
    assert len(errors) == 0


def test_response(db_conn, responses_table):
    """
    Expect to record the user's response.
    """

    response, errors = Response.insert(db_conn, {
        'user_id': 'A',
        'card_id': 'BC',
        'unit_id': 'RM',
        'score': 0.9,
        'learned': 0.9,
    })
    assert len(errors) == 1
    response['response'] = 42
    response, errors = response.save(db_conn)
    assert len(errors) == 0


def test_score(db_conn, responses_table):
    """
    Expect to have a score between 0 and 1 (including).
    """

    response, errors = Response.insert(db_conn, {
        'user_id': 'A',
        'card_id': 'BC',
        'unit_id': 'RM',
        'response': 42,
        'learned': 0.9,
    })
    assert len(errors) == 1
    response['score'] = 1.1
    response, errors = response.save(db_conn)
    assert len(errors) == 1
    response['score'] = 0
    response, errors = response.save(db_conn)
    assert len(errors) == 0
    response['score'] = 1
    response, errors = response.save(db_conn)
    assert len(errors) == 0


def test_get_latest(db_conn, responses_table):
    """
    Expect to get the latest response by user and unit.
    """

    responses_table.insert([{
        'id': 'A',
        'user_id': 'abcd1234',
        'unit_id': 'apple',
        'created': r.now(),
        'modified': r.now(),
    }, {
        'id': 'B',
        'user_id': 'abcd1234',
        'unit_id': 'banana',
        'created': r.now(),
        'modified': r.now(),
    }]).run(db_conn)

    assert Response.get_latest(db_conn, 'abcd1234', 'apple')['id'] == 'A'
