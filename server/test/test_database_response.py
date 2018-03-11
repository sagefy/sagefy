import uuid

from database.response import insert_response, \
  get_latest_response, \
  deliver_response
from raw_insert import raw_insert_users, \
  raw_insert_units, \
  raw_insert_cards, \
  raw_insert_responses
from modules.util import convert_uuid_to_slug




user_a_uuid = uuid.uuid4()
test_unit_uuid = uuid.uuid4()
test_card_uuid = uuid.uuid4()
test_card_option1_uuid = uuid.uuid4()
test_card_option2_uuid = uuid.uuid4()


def create_response_test_data(db_conn):
  users = [{
    'id': user_a_uuid,
    'name': 'test',
    'email': 'test@example.com',
    'password': 'abcd1234',
  }]
  raw_insert_users(db_conn, users)
  units = [{
    'entity_id': test_unit_uuid,
    'name': 'Calculus',
    'user_id': user_a_uuid,
    'body': 'Calculus is fun sometimes.',
  }]
  raw_insert_units(db_conn, units)
  cards = [{
    'user_id': user_a_uuid,
    'entity_id': test_card_uuid,
    'unit_id': test_unit_uuid,
    'kind': 'choice',
    'name': 'Meaning of Life',
    'data': {
      'body': 'What is the meaning of life?',
      'options': [{
        'id': convert_uuid_to_slug(test_card_option1_uuid),
        'value': '42',
        'correct': True,
        'feedback': 'Yay!',
      }, {
        'id': convert_uuid_to_slug(test_card_option2_uuid),
        'value': 'love',
        'correct': False,
        'feedback': 'Boo!',
      }],
      'order': 'set',
      'max_options_to_show': 4,
    },
  }]
  raw_insert_cards(db_conn, cards)
  responses = [{
    'user_id': user_a_uuid,
    'card_id': test_card_uuid,
    'unit_id': test_unit_uuid,
    'response': test_card_option1_uuid,
    'score': 1,
    'learned': 0.5,
  }, {
    'user_id': user_a_uuid,
    'card_id': test_card_uuid,
    'unit_id': test_unit_uuid,
    'response': test_card_option2_uuid,
    'score': 0,
    'learned': 0.4,
  }]
  raw_insert_responses(db_conn, responses)


def test_insert_response(db_conn):
  create_response_test_data(db_conn)
  response, errors = insert_response(db_conn, {
    'user_id': user_a_uuid,
    'card_id': test_card_uuid,
    'unit_id': test_unit_uuid,
    'response': convert_uuid_to_slug(test_card_option1_uuid),
    'score': 1,
    'learned': 0.6,
  })
  assert not errors
  assert response


def test_get_latest_response(db_conn):
  create_response_test_data(db_conn)
  response = get_latest_response(
    db_conn,
    user_id=user_a_uuid,
    unit_id=test_unit_uuid
  )
  assert response
  assert response['score'] == 0


def test_deliver_response(db_conn):
  create_response_test_data(db_conn)
  response = get_latest_response(
    db_conn,
    user_id=user_a_uuid,
    unit_id=test_unit_uuid
  )
  result = deliver_response(response, access=None)
  assert result
