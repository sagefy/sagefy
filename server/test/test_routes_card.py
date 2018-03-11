import uuid
from datetime import datetime, timezone
import json
from framework.redis_conn import red
import routes.card  # TODO-2 switch to direct imports
from conftest import user_id
from raw_insert import raw_insert_cards, raw_insert_units
from modules.util import convert_uuid_to_slug


entity_id = uuid.uuid4()
entity_id_r = uuid.uuid4()
entity_id_b = uuid.uuid4()
unit_id = uuid.uuid4()
card_id = uuid.uuid4()
good_response_id = uuid.uuid4()
card_version_id = uuid.uuid4()


def create_test_cards(db_conn):
  units = [{
    'entity_id': unit_id,
    'status': 'accepted',
    'name': 'Wildwood',
    'body': 'Wildwood',
  }]
  raw_insert_units(db_conn, units)

  cards = [{
    'entity_id': entity_id,
    'unit_id': unit_id,
    'status': 'accepted',
    'kind': 'video',
    'name': 'Video A',
    'require_ids': [entity_id_r],
  }, {
    'entity_id': entity_id,
    'unit_id': unit_id,
    'created': datetime(1986, 11, 3, tzinfo=timezone.utc),
    'modified': datetime(1986, 11, 3, tzinfo=timezone.utc),
    'status': 'accepted',
    'kind': 'video',
    'name': 'Video A',
  }, {
    'entity_id': entity_id_r,
    'unit_id': unit_id,
    'status': 'accepted',
    'kind': 'video',
    'name': 'Video Z',
  }, {
    'entity_id': entity_id_b,
    'unit_id': unit_id,
    'status': 'accepted',
    'kind': 'choice',
    'require_ids': [entity_id],
    'name': 'Video X',
  }, {
    'version_id': card_version_id,
    'entity_id': card_id,
    'unit_id': unit_id,
    'status': 'accepted',
    'kind': 'choice',
    'name': 'Meaning of Life',
    'data': {
      'body': 'What is the meaning of life?',
      'options': [{
        'id': convert_uuid_to_slug(good_response_id),
        'value': '42',
        'correct': True,
        'feedback': 'Yay!',
      }, {
        'id': convert_uuid_to_slug(uuid.uuid4()),
        'value': 'love',
        'correct': False,
        'feedback': 'Boo!',
      }],
      'order': 'set',
      'max_options_to_show': 4,
    },
  }, {
    'entity_id': uuid.uuid4(),
    'unit_id': unit_id,
    'status': 'accepted',
    'kind': 'choice',
    'name': 'Meaning of Love',
    'data': {
      'body': 'What is the meaning of love?',
      'options': [{
        'id': convert_uuid_to_slug(uuid.uuid4()),
        'value': 'Flava Flav',
        'correct': True,
        'feedback': 'Yay!',
      }, {
        'id': convert_uuid_to_slug(uuid.uuid4()),
        'value': 'life',
        'correct': False,
        'feedback': 'Boo!',
      }],
      'order': 'set',
      'max_options_to_show': 4,
    },
  }]
  raw_insert_cards(db_conn, cards)


def test_get_card(db_conn, session):
  """
  Expect to get the card information for displaying to a contributor.
  """

  create_test_cards(db_conn)
  code, response = routes.card.get_card_route({
    'db_conn': db_conn
  }, convert_uuid_to_slug(entity_id))
  assert code == 200
  # Model
  assert response['card']['entity_id'] == entity_id
  assert response['card']['kind'] == 'video'
  # Unit
  assert response['unit']['name'] == 'Wildwood'
  # Requires
  assert len(response['requires']) == 1
  assert response['requires'][0]['entity_id'] == entity_id_r
  # Required By
  assert len(response['required_by']) == 1
  assert response['required_by'][0]['entity_id'] == entity_id_b
  # TODO-3 sequencer data: learners, transit, guess, slip, difficulty


def test_get_card_404(db_conn):
  """
  Expect to fail to get an unknown card. (404)
  """

  code, _ = routes.card.get_card_route({
    'db_conn': db_conn
  }, convert_uuid_to_slug(uuid.uuid4()))
  assert code == 404


def test_list_cards_route(db_conn, session):
  create_test_cards(db_conn)
  request = {
    'db_conn': db_conn,
    'params': {
      'entity_ids': convert_uuid_to_slug(entity_id),
    },
  }
  code, _ = routes.card.list_cards_route(request)
  assert code == 200


def test_learn_card(db_conn, session):
  """
  Expect to get a card for learn mode. (200)
  """

  create_test_cards(db_conn)
  redis_key = 'learning_context_{user_id}'.format(
    user_id=convert_uuid_to_slug(user_id)
  )
  red.set(
    redis_key,
    json.dumps({
      'unit': {'entity_id': convert_uuid_to_slug(unit_id)},
    })
  )
  request = {'cookies': {'session_id': session}, 'db_conn': db_conn}
  code, response = routes.card.learn_card_route(
    request,
    convert_uuid_to_slug(card_id)
  )
  red.delete(redis_key)
  assert not response.get('errors')
  assert code == 200
  assert 'order' not in response['card']
  # TODO-3 assert 'correct' not in response['card']['options'][0]
  # TODO-3 assert 'feedback' not in response['card']['options'][0]
  assert 'subject' in response
  assert 'unit' in response


def test_learn_card_401(db_conn):
  """
  Expect to require log in to get a card for learn mode. (401)
  """

  code, _ = routes.card.learn_card_route({
    'db_conn': db_conn
  }, convert_uuid_to_slug(uuid.uuid4()))
  assert code == 401


def test_learn_card_404(db_conn, session):
  """
  Expect to fail to get an unknown card for learn mode. (404)
  """

  request = {'cookies': {'session_id': session}, 'db_conn': db_conn}
  code, _ = routes.card.learn_card_route(
    request,
    convert_uuid_to_slug(uuid.uuid4())
  )
  assert code == 404


def test_learn_card_400(db_conn, session):
  """
  Expect the card for learn mode to make sense,
  given the learner context. (400)
  """

  create_test_cards(db_conn)
  redis_key = 'learning_context_{user_id}'.format(
    user_id=convert_uuid_to_slug(user_id)
  )
  red.set(
    redis_key,
    json.dumps({
      'unit': {'entity_id': convert_uuid_to_slug(uuid.uuid4())},
    })
  )
  request = {'cookies': {'session_id': session}, 'db_conn': db_conn}
  code, _ = routes.card.learn_card_route(
    request,
    convert_uuid_to_slug(card_id)
  )
  red.delete(redis_key)
  assert code == 400


def test_get_card_versions_route(db_conn, session):
  create_test_cards(db_conn)
  request = {
    'db_conn': db_conn
  }
  code, response = routes.card.get_card_versions_route(request, card_id)
  assert not response.get('errors')
  assert code == 200
  assert response['versions']


def test_get_card_version_route(db_conn, session):
  create_test_cards(db_conn)
  request = {
    'db_conn': db_conn
  }
  version_id = card_version_id
  code, response = routes.card.get_card_version_route(request, version_id)
  assert not response.get('errors')
  assert code == 200
  assert response['version']


def test_respond_card(db_conn, session):
  """
  Expect to respond to a card. (200)
  """

  create_test_cards(db_conn)
  redis_key = 'learning_context_{user_id}'.format(
    user_id=convert_uuid_to_slug(user_id)
  )
  red.set(
    redis_key,
    json.dumps({
      'card': {'entity_id': convert_uuid_to_slug(card_id)},
      'unit': {'entity_id': convert_uuid_to_slug(unit_id)},
    })
  )
  request = {
    'params': {'response': convert_uuid_to_slug(good_response_id)},
    'cookies': {'session_id': session},
    'db_conn': db_conn,
  }
  code, response = routes.card.respond_to_card_route(request, card_id)
  red.delete(redis_key)
  assert not response.get('errors')
  assert code == 200
  assert 'response' in response
  assert 'feedback' in response


def test_respond_card_401(db_conn):
  """
  Expect to require log in to get an unknown card. (401)
  """

  code, _ = routes.card.respond_to_card_route({
    'db_conn': db_conn
  }, convert_uuid_to_slug(uuid.uuid4()))
  assert code == 401


def test_respond_card_404(db_conn, session):
  """
  Expect to fail to respond to an unknown card. (404)
  """

  code, _ = routes.card.respond_to_card_route({
    'params': {'response': convert_uuid_to_slug(uuid.uuid4())},
    'cookies': {'session_id': session},
    'db_conn': db_conn,
  }, convert_uuid_to_slug(uuid.uuid4()))
  assert code == 404


def test_respond_card_400a(db_conn, session):
  """
  Expect the card being responded to make sense,
  given the learner context. (400)
  """

  create_test_cards(db_conn)
  redis_key = 'learning_context_{user_id}'.format(
    user_id=convert_uuid_to_slug(user_id)
  )
  red.set(
    redis_key,
    json.dumps({
      'card': {'entity_id': convert_uuid_to_slug(uuid.uuid4())},
      'unit': {'entity_id': convert_uuid_to_slug(unit_id)},
    })
  )
  request = {
    'params': {'response': convert_uuid_to_slug(good_response_id)},
    'cookies': {'session_id': session},
    'db_conn': db_conn,
  }
  code, response = routes.card.respond_to_card_route(request, card_id)
  red.delete(redis_key)
  assert code == 400
  assert 'errors' in response


def test_respond_card_400b(db_conn, session):
  """
  Expect response to a card to make sense. (400)
  """

  create_test_cards(db_conn)
  redis_key = 'learning_context_{user_id}'.format(
    user_id=convert_uuid_to_slug(user_id)
  )
  red.set(
    redis_key,
    json.dumps({
      'card': {'entity_id': convert_uuid_to_slug(card_id)},
      'unit': {'entity_id': convert_uuid_to_slug(unit_id)},
    })
  )
  request = {
    'params': {'response': convert_uuid_to_slug(uuid.uuid4())},
    'cookies': {'session_id': session},
    'db_conn': db_conn,
  }
  code, response = routes.card.respond_to_card_route(request, card_id)
  red.delete(redis_key)
  assert code == 400
  assert 'errors' in response


def test_create_new_card_version_route(db_conn, session):
  create_test_cards(db_conn)
  request = {
    'cookies': {'session_id': session},
    'db_conn': db_conn,
    'params': {
      'unit_id': unit_id,
      'kind': 'video',
      'name': 'Video Z',
      'data': {
        'site': 'youtube',
        'video_id': 'whatever',
      },
    }
  }
  code, response = routes.card.create_new_card_version_route(request)
  assert not response.get('errors')
  assert code == 200
  assert response['version']


def test_create_existing_card_version_route(db_conn, session):
  create_test_cards(db_conn)
  request = {
    'params': {
      'data': {
        'site': 'youtube',
        'video_id': 'whatever',
      },
    },
    'cookies': {'session_id': session},
    'db_conn': db_conn,
  }
  code, response = routes.card.create_existing_card_version_route(
    request,
    entity_id_r
  )
  assert not response.get('errors')
  assert code == 200
  assert response['version']
