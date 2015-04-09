import rethinkdb as r
import json
import routes.card
from framework.redis import redis
import pytest

xfail = pytest.mark.xfail


def test_get_card(db_conn, cards_table, units_table, topics_table):
    """
    Expect to get the card information for displaying to a contributor.
    """

    cards_table.insert([{
        'entity_id': 'abcd',
        'unit_id': 'zytx',
        'created': r.now(),
        'modified': r.now(),
        'canonical': True,
        'kind': 'video',
        'requires': ['zxyz'],
    }, {
        'entity_id': 'abcd',
        'unit_id': 'zytx',
        'created': r.time(1986, 11, 3, 'Z'),
        'modified': r.time(1986, 11, 3, 'Z'),
        'canonical': True,
        'kind': 'video',
    }, {
        'entity_id': 'zxyz',
        'unit_id': 'zytx',
        'created': r.now(),
        'modified': r.now(),
        'canonical': True,
        'kind': 'video',
    }, {
        'entity_id': 'qwer',
        'unit_id': 'zytx',
        'created': r.now(),
        'modified': r.now(),
        'canonical': True,
        'kind': 'choice',
        'requires': ['abcd'],
    }]).run(db_conn)

    units_table.insert({
        'entity_id': 'zytx',
        'created': r.now(),
        'modified': r.now(),
        'canonical': True,
        'name': 'Wildwood',
    }).run(db_conn)

    topics_table.insert([{
        'created': r.now(),
        'modified': r.now(),
        'user_id': 'abcd1234',
        'name': 'A Modest Proposal',
        'entity': {
            'id': 'abcd',
            'kind': 'card'
        }
    }, {
        'created': r.now(),
        'modified': r.now(),
        'user_id': 'abcd1234',
        'name': 'Another Proposal',
        'entity': {
            'id': 'abcd',
            'kind': 'card'
        }
    }]).run(db_conn)

    code, response = routes.card.get_card_route({}, 'abcd')
    assert code == 200
    # Model
    assert response['card']['entity_id'] == 'abcd'
    assert response['card']['kind'] == 'video'
    # Unit
    assert response['unit']['name'] == 'Wildwood'
    # Versions
    assert len(response['versions']) == 2
    assert response['versions'][0]['kind'] == 'video'
    # Topics
    assert len(response['topics']) == 2
    assert response['topics'][0]['entity']['id'] == 'abcd'
    # Requires
    assert len(response['requires']) == 1
    assert response['requires'][0]['entity_id'] == 'zxyz'
    # Required By
    assert len(response['required_by']) == 1
    assert response['required_by'][0]['entity_id'] == 'qwer'
    # TODO@ sequencer data: learners, transit, guess, slip, difficulty


def test_get_card_404(db_conn):
    """
    Expect to fail to get an unknown card. (404)
    """

    code, response = routes.card.get_card_route({}, 'abcd')
    assert code == 404


def test_learn_card(db_conn, session, cards_table):
    """
    Expect to get a card for learn mode. (200)
    """

    cards_table.insert({
        'entity_id': 'tyui4567',
        'unit_id': 'vbnm7890',
        'created': r.now(),
        'modified': r.now(),
        'canonical': True,
        'kind': 'choice',
        'name': 'Meaning of Life',
        'body': 'What is the meaning of life?',
        'options': [{
            'value': '42',
            'correct': True,
            'feedback': 'Yay!',
        }, {
            'value': 'love',
            'correct': False,
            'feedback': 'Boo!',
        }],
        'order': 'set',
        'max_options_to_show': 4,
    }).run(db_conn)

    redis.set('learning_context_abcd1234', json.dumps({
        'unit': {'id': 'vbnm7890'},
        'set': {'id': 'jkl;1234'},
    }))

    response = session.get('/api/cards/tyui4567/learn/')
    assert response.status_code == 200
    response = json.loads(response.data.decode())
    assert 'order' not in response['card']
    # TODO@ assert 'correct' not in response['card']['options'][0]
    # TODO@ assert 'feedback' not in response['card']['options'][0]
    assert 'set' in response
    assert 'unit' in response

    redis.delete('learning_context_abcd1234')


def test_learn_card_401(db_conn):
    """
    Expect to require log in to get a card for learn mode. (401)
    """

    response = app.test_client().get('/api/cards/abcd/learn/')
    assert response.status_code == 401


def test_learn_card_404(db_conn, session):
    """
    Expect to fail to get an unknown card for learn mode. (404)
    """

    response = session.get('/api/cards/abcd/learn/')
    assert response.status_code == 404


def test_learn_card_400(db_conn, cards_table, session):
    """
    Expect the card for learn mode to make sense,
    given the learner context. (400)
    """

    cards_table.insert({
        'entity_id': 'tyui4567',
        'unit_id': 'vbnm7890',
        'created': r.now(),
        'modified': r.now(),
        'canonical': True,
        'kind': 'choice',
        'name': 'Meaning of Life',
        'body': 'What is the meaning of life?',
        'options': [{
            'value': '42',
            'correct': True,
            'feedback': 'Yay!',
        }, {
            'value': 'love',
            'correct': False,
            'feedback': 'Boo!',
        }],
        'order': 'set',
        'max_options_to_show': 4,
    }).run(db_conn)

    redis.set('learning_context_abcd1234', json.dumps({
        'unit': {'id': 'gfds6543'},
        'set': {'id': '6543hgfs'},
    }))

    response = session.get('/api/cards/tyui4567/learn/')
    assert response.status_code == 400
    response = json.loads(response.data.decode())
    redis.delete('learning_context_abcd1234')


def test_respond_card(db_conn, cards_table, session):
    """
    Expect to respond to a card. (200)
    """

    cards_table.insert({
        'entity_id': 'tyui4567',
        'unit_id': 'vbnm7890',
        'created': r.now(),
        'modified': r.now(),
        'canonical': True,
        'kind': 'choice',
        'name': 'Meaning of Life',
        'body': 'What is the meaning of life?',
        'options': [{
            'value': '42',
            'correct': True,
            'feedback': 'Yay!',
        }, {
            'value': 'love',
            'correct': False,
            'feedback': 'Boo!',
        }],
        'order': 'set',
        'max_options_to_show': 4,
    }).run(db_conn)

    redis.set('learning_context_abcd1234', json.dumps({
        'unit': {'id': 'vbnm7890'},
        'set': {'id': 'jkl;1234'},
        'card': {'id': 'tyui4567'},
    }))

    response = session.post('/api/cards/tyui4567/responses/', data=json.dumps({
        'response': '42'
    }), content_type='application/json')
    assert response.status_code == 200
    response = json.loads(response.data.decode())
    assert 'response' in response
    assert 'feedback' in response
    redis.delete('learning_context_abcd1234')


def test_respond_card_401(db_conn):
    """
    Expect to require log in to get an unknown card. (401)
    """

    response = app.test_client().post('/api/cards/abcd/responses/')
    assert response.status_code == 401


def test_respond_card_404(db_conn, session):
    """
    Expect to fail to respond to an unknown card. (404)
    """

    response = session.post('/api/cards/abcd/responses/')
    assert response.status_code == 404


def test_respond_card_400a(db_conn, session, cards_table):
    """
    Expect the card being responded to make sense,
    given the learner context. (400)
    """

    cards_table.insert({
        'entity_id': 'tyui4567',
        'unit_id': 'vbnm7890',
        'created': r.now(),
        'modified': r.now(),
        'canonical': True,
        'kind': 'choice',
        'name': 'Meaning of Life',
        'body': 'What is the meaning of life?',
        'options': [{
            'value': '42',
            'correct': True,
            'feedback': 'Yay!',
        }, {
            'value': 'love',
            'correct': False,
            'feedback': 'Boo!',
        }],
        'order': 'set',
        'max_options_to_show': 4,
    }).run(db_conn)

    redis.set('learning_context_abcd1234', json.dumps({
        'unit': {'id': 'vbnm7890'},
        'set': {'id': 'jkl;1234'},
        'card': {'id': 'gfds3456'},
    }))

    response = session.post('/api/cards/tyui4567/responses/', data=json.dumps({
        'response': '42'
    }), content_type='application/json')
    assert response.status_code == 400
    response = json.loads(response.data.decode())
    redis.delete('learning_context_abcd1234')


def test_respond_card_400b(db_conn, session, cards_table):
    """
    Expect response to a card to make sense. (400)
    """

    cards_table.insert({
        'entity_id': 'tyui4567',
        'unit_id': 'vbnm7890',
        'created': r.now(),
        'modified': r.now(),
        'canonical': True,
        'kind': 'choice',
        'name': 'Meaning of Life',
        'body': 'What is the meaning of life?',
        'options': [{
            'value': '42',
            'correct': True,
            'feedback': 'Yay!',
        }, {
            'value': 'love',
            'correct': False,
            'feedback': 'Boo!',
        }],
        'order': 'set',
        'max_options_to_show': 4,
    }).run(db_conn)

    redis.set('learning_context_abcd1234', json.dumps({
        'unit': {'id': 'vbnm7890'},
        'set': {'id': 'jkl;1234'},
        'card': {'id': 'tyui4567'},
    }))

    response = session.post('/api/cards/tyui4567/responses/', data=json.dumps({
        'response': 'Waffles'
    }), content_type='application/json')
    assert response.status_code == 400
    response = json.loads(response.data.decode())
    assert 'errors' in response
    redis.delete('learning_context_abcd1234')
