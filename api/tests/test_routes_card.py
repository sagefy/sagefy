import pytest

xfail = pytest.mark.xfail

import rethinkdb as r


@xfail
def test_get_card(app, db_conn,
                  cards_table, units_table, topics_table):
    """
    Expect to get the card information for displaying to a contributor.
    """

    cards_table.insert({
        'entity_id': 'abcd',
        'unit_id': 'abcd',
        'created': r.now(),
        'modified': r.now(),
        'canonical': True,
        'kind': 'video',
    }).run(db_conn)
    response = app.test_client().get('/api/cards/abcd/')
    assert response.status_code == 200
    response = response.data.decode('utf-8')
    assert response['card']['entity_id'] == 'abcd'
    assert response['card']['kind'] == 'video'
    # TODO@ get unit data
    # TODO@ join through requires both ways
    # TODO@ list of topics
    # TODO@ list of versions
    # TODO@ sequencer data: learners, transit, guess, slip, difficulty


def test_get_card_404(app, db_conn):
    """
    Expect to fail to get an unknown card. (404)
    """

    response = app.test_client().get('/api/cards/abcd/')
    assert response.status_code == 404


@xfail
def test_learn_card():
    """
    Expect to get a card for learn mode. (200)
    """

    assert False


@xfail
def test_learn_card_relevant():
    """
    Expect to learn card to only provide relevant data. (200)
    """

    assert False


@xfail
def test_learn_card_401():
    """
    Expect to require log in to get a card for learn mode. (401)
    """

    assert False


@xfail
def test_learn_card_404():
    """
    Expect to fail to get an unknown card for learn mode. (404)
    """

    assert False


@xfail
def test_learn_card_400():
    """
    Expect the card for learn mode to make sense,
    given the learner context. (400)
    """

    assert False


@xfail
def test_respond_card():
    """
    Expect to respond to a card. (200)
    """

    assert False


@xfail
def test_respond_card_401():
    """
    Expect to require log in to get an unknown card. (401)
    """

    assert False


@xfail
def test_respond_card_404():
    """
    Expect to fail to respond to an unknown card. (404)
    """

    assert False


@xfail
def test_respond_card_400():
    """
    Expect respond to a card to make sense. (400)
    """

    assert False
