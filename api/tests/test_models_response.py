from models.response import Response


def test_created(app, db_conn, responses_table):
    """
    Expect to have a created date.
    """

    response = Response({
        'user_id': 'A',
        'card_id': 'BC',
        'unit_id': 'RM',
        'response': 42,
        'score': 0.9,
    })
    del response['created']  # should be set to default anywho
    response, errors = response.save()
    assert len(errors) == 0


def test_user(app, db_conn, responses_table):
    """
    Expect to require a user ID.
    """

    response, errors = Response.insert({
        'card_id': 'BC',
        'unit_id': 'RM',
        'response': 42,
        'score': 0.9,
    })
    assert len(errors) == 1
    response['user_id'] = 'A'
    response, errors = response.save()
    assert len(errors) == 0


def test_card(app, db_conn, responses_table):
    """
    Expect to require a card ID.
    """

    response, errors = Response.insert({
        'user_id': 'A',
        'unit_id': 'RM',
        'response': 42,
        'score': 0.9,
    })
    assert len(errors) == 1
    response['card_id'] = 'AFJ'
    response, errors = response.save()
    assert len(errors) == 0


def test_unit(app, db_conn, responses_table):
    """
    Expect to require a unit ID.
    """

    response, errors = Response.insert({
        'user_id': 'A',
        'card_id': 'BC',
        'response': 42,
        'score': 0.9,
    })
    assert len(errors) == 1
    response['unit_id'] = 'A24JLD'
    response, errors = response.save()
    assert len(errors) == 0


def test_response(app, db_conn, responses_table):
    """
    Expect to record the user's response.
    """

    response, errors = Response.insert({
        'user_id': 'A',
        'card_id': 'BC',
        'unit_id': 'RM',
        'score': 0.9,
    })
    assert len(errors) == 1
    response['response'] = 42
    response, errors = response.save()
    assert len(errors) == 0


def test_score(app, db_conn, responses_table):
    """
    Expect to have a score between 0 and 1 (including).
    """

    response, errors = Response.insert({
        'user_id': 'A',
        'card_id': 'BC',
        'unit_id': 'RM',
        'response': 42,
    })
    assert len(errors) == 1
    response['score'] = 1.1
    response, errors = response.save()
    assert len(errors) == 1
    response['score'] = 0
    response, errors = response.save()
    assert len(errors) == 0
    response['score'] = 1
    response, errors = response.save()
    assert len(errors) == 0
