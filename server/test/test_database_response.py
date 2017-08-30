from database.response import insert_response, get_latest_response



def test_created(db_conn, responses_table):
    """
    Expect to have a created date.
    """

    response, errors = insert_response({
        'user_id': 'A',
        'card_id': 'BC',
        'unit_id': 'RM',
        'response': 42,
        'score': 0.9,
        'learned': 0.9,
    }, db_conn)
    assert len(errors) == 0
    assert response['created']


def test_user(db_conn, responses_table):
    """
    Expect to require a user ID.
    """

    repsonse_data = {
        'card_id': 'BC',
        'unit_id': 'RM',
        'response': 42,
        'score': 0.9,
        'learned': 0.9,
    }
    response, errors = insert_response(db_conn, repsonse_data)
    assert len(errors) == 1
    repsonse_data['user_id'] = 'A'
    response, errors = insert_response(db_conn, repsonse_data)
    assert len(errors) == 0


def test_card(db_conn, responses_table):
    """
    Expect to require a card ID.
    """

    response_data = {
        'user_id': 'A',
        'unit_id': 'RM',
        'response': 42,
        'score': 0.9,
        'learned': 0.9,
    }
    response, errors = insert_response(db_conn, response_data)
    assert len(errors) == 1
    response_data['card_id'] = 'AFJ'
    response, errors = insert_response(db_conn, response_data)
    assert len(errors) == 0


def test_unit(db_conn, responses_table):
    """
    Expect to require a unit ID.
    """

    response_data = {
        'user_id': 'A',
        'card_id': 'BC',
        'response': 42,
        'score': 0.9,
        'learned': 0.9,
    }
    response, errors = insert_response(db_conn, response_data)
    assert len(errors) == 1
    response_data['unit_id'] = 'A24JLD'
    response, errors = insert_response(db_conn, response_data)
    assert len(errors) == 0


def test_response(db_conn, responses_table):
    """
    Expect to record the user's response.
    """

    response_data = {
        'user_id': 'A',
        'card_id': 'BC',
        'unit_id': 'RM',
        'score': 0.9,
        'learned': 0.9,
    }
    response, errors = insert_response(db_conn, response_data)
    assert len(errors) == 1
    response_data['response'] = 42
    response, errors = insert_response(db_conn, response_data)
    assert len(errors) == 0


def test_score(db_conn, responses_table):
    """
    Expect to have a score between 0 and 1 (including).
    """

    response_data = {
        'user_id': 'A',
        'card_id': 'BC',
        'unit_id': 'RM',
        'response': 42,
        'learned': 0.9,
    }
    response, errors = insert_response(db_conn, response_data)
    assert len(errors) == 1
    response_data['score'] = 1.1
    response, errors = insert_response(db_conn, response_data)
    assert len(errors) == 1
    response_data['score'] = 0
    response, errors = insert_response(db_conn, response_data)
    assert len(errors) == 0
    response_data['score'] = 1
    response, errors = insert_response(db_conn, response_data)
    assert len(errors) == 0


def test_get_latest(db_conn, responses_table):
    """
    Expect to get the latest response by user and unit.
    """

    responses_table.insert([{
        'id': 'A',
        'user_id': 'abcd1234',
        'unit_id': 'apple',
        'created': datetime.utcnow(),
        'modified': datetime.utcnow(),
    }, {
        'id': 'B',
        'user_id': 'abcd1234',
        'unit_id': 'banana',
        'created': datetime.utcnow(),
        'modified': datetime.utcnow(),
    }]).run(db_conn)

    assert get_latest_response(db_conn, 'abcd1234', 'apple')['id'] == 'A'
