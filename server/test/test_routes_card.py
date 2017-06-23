import rethinkdb as r
import json
import routes.card
from framework.redis import redis
import pytest

xfail = pytest.mark.xfail


def test_get_card(db_conn, cards_table, cards_parameters_table, units_table,
                  topics_table):
    """
    Expect to get the card information for displaying to a contributor.
    """

    cards_table.insert([{
        'entity_id': 'abcd',
        'unit_id': 'zytx',
        'created': r.now(),
        'modified': r.now(),
        'status': 'accepted',
        'kind': 'video',
        'require_ids': ['zxyz'],
    }, {
        'entity_id': 'abcd',
        'unit_id': 'zytx',
        'created': r.time(1986, 11, 3, 'Z'),
        'modified': r.time(1986, 11, 3, 'Z'),
        'status': 'accepted',
        'kind': 'video',
    }, {
        'entity_id': 'zxyz',
        'unit_id': 'zytx',
        'created': r.now(),
        'modified': r.now(),
        'status': 'accepted',
        'kind': 'video',
    }, {
        'entity_id': 'qwer',
        'unit_id': 'zytx',
        'created': r.now(),
        'modified': r.now(),
        'status': 'accepted',
        'kind': 'choice',
        'require_ids': ['abcd'],
    }]).run(db_conn)

    cards_parameters_table.insert({
        'entity_id': 'abcd',
    }).run(db_conn)

    units_table.insert({
        'entity_id': 'zytx',
        'created': r.now(),
        'modified': r.now(),
        'status': 'accepted',
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

    code, response = routes.card.get_card_route({
        'db_conn': db_conn
    }, 'abcd')
    assert code == 200
    # Model
    assert response['card']['entity_id'] == 'abcd'
    assert response['card']['kind'] == 'video'
    # Unit
    assert response['unit']['name'] == 'Wildwood'
    # Requires
    assert len(response['requires']) == 1
    assert response['requires'][0]['entity_id'] == 'zxyz'
    # Required By
    assert len(response['required_by']) == 1
    assert response['required_by'][0]['entity_id'] == 'qwer'
    # TODO-3 sequencer data: learners, transit, guess, slip, difficulty


def test_get_card_404(db_conn):
    """
    Expect to fail to get an unknown card. (404)
    """

    code, response = routes.card.get_card_route({
        'db_conn': db_conn
    }, 'abcd')
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
        'status': 'accepted',
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
        'unit': {'entity_id': 'vbnm7890'},
        'subject': {'entity_id': 'jkl;1234'},
    }))

    request = {'cookies': {'session_id': session}, 'db_conn': db_conn}
    code, response = routes.card.learn_card_route(request, 'tyui4567')
    assert code == 200
    assert 'order' not in response['card']
    # TODO-3 assert 'correct' not in response['card']['options'][0]
    # TODO-3 assert 'feedback' not in response['card']['options'][0]
    assert 'subject' in response
    assert 'unit' in response

    redis.delete('learning_context_abcd1234')


def test_learn_card_401(db_conn):
    """
    Expect to require log in to get a card for learn mode. (401)
    """

    code, response = routes.card.learn_card_route({
        'db_conn': db_conn
    }, 'abcd')
    assert code == 401


def test_learn_card_404(db_conn, session):
    """
    Expect to fail to get an unknown card for learn mode. (404)
    """

    request = {'cookies': {'session_id': session}, 'db_conn': db_conn}
    code, response = routes.card.learn_card_route(request, 'abcd')
    assert code == 404


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
        'status': 'accepted',
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
        'unit': {'entity_id': 'gfds6543'},
        'subject': {'entity_id': '6543hgfs'},
    }))

    request = {'cookies': {'session_id': session}, 'db_conn': db_conn}
    code, response = routes.card.learn_card_route(request, 'tyui4567')
    assert code == 400
    redis.delete('learning_context_abcd1234')


def test_respond_card(db_conn, units_table, cards_table,
                      cards_parameters_table,
                      responses_table, session):
    """
    Expect to respond to a card. (200)
    """

    cards_table.insert([{
        'entity_id': 'tyui4567',
        'unit_id': 'vbnm7890',
        'created': r.now(),
        'modified': r.now(),
        'status': 'accepted',
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
    }, {
        'entity_id': 'abcd1234',
        'unit_id': 'vbnm7890',
        'created': r.now(),
        'modified': r.now(),
        'status': 'accepted',
        'kind': 'choice',
        'name': 'Meaning of Love',
        'body': 'What is the meaning of love?',
        'options': [{
            'value': 'Flava Flav',
            'correct': True,
            'feedback': 'Yay!',
        }, {
            'value': 'life',
            'correct': False,
            'feedback': 'Boo!',
        }],
        'order': 'set',
        'max_options_to_show': 4,
    }]).run(db_conn)

    units_table.insert({
        'entity_id': 'vbnm7890',
        'created': r.now(),
    }).run(db_conn)

    redis.set('learning_context_abcd1234', json.dumps({
        'subject': {'entity_id': 'jkl;1234'},
        'card': {'entity_id': 'tyui4567'},
        'unit': {'entity_id': 'vbnm7890'},
    }))

    request = {
        'params': {'response': '42'},
        'cookies': {'session_id': session},
        'db_conn': db_conn,
    }
    code, response = routes.card.respond_to_card_route(request, 'tyui4567')

    assert code == 200
    assert 'response' in response
    assert 'feedback' in response
    redis.delete('learning_context_abcd1234')


def test_respond_card_401(db_conn):
    """
    Expect to require log in to get an unknown card. (401)
    """

    code, response = routes.card.respond_to_card_route({
        'db_conn': db_conn
    }, 'abcd')
    assert code == 401


def test_respond_card_404(db_conn, session):
    """
    Expect to fail to respond to an unknown card. (404)
    """

    request = {
        'params': {'response': '42'},
        'cookies': {'session_id': session},
        'db_conn': db_conn,
    }
    code, response = routes.card.respond_to_card_route(request, 'abcd')
    assert code == 404


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
        'status': 'accepted',
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
        'unit': {'entity_id': 'vbnm7890'},
        'subject': {'entity_id': 'jkl;1234'},
        'card': {'entity_id': 'gfds3456'},
    }))

    request = {
        'params': {'response': '42'},
        'cookies': {'session_id': session},
        'db_conn': db_conn,
    }
    code, response = routes.card.respond_to_card_route(request, 'tyui4567')
    assert code == 400
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
        'status': 'accepted',
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
        'unit': {'entity_id': 'vbnm7890'},
        'subject': {'entity_id': 'jkl;1234'},
        'card': {'entity_id': 'tyui4567'},
    }))

    request = {
        'params': {'response': 'Waffles'},
        'cookies': {'session_id': session},
        'db_conn': db_conn
    }
    code, response = routes.card.respond_to_card_route(request, 'tyui4567')
    assert code == 400
    assert 'errors' in response
    redis.delete('learning_context_abcd1234')


@xfail
def test_respond_card_diag():
    """
    Expect diagnosis to not show feedback to responses.
    """

    assert False
