
import uuid

from database.card import get_card_schema, \
  ensure_requires, \
  ensure_no_cycles, \
  insert_card, \
  insert_card_version, \
  update_card, \
  validate_card_response, \
  score_card_response, \
  deliver_card, \
  get_latest_accepted_card, \
  list_latest_accepted_cards, \
  list_many_card_versions, \
  get_card_version, \
  list_one_card_versions, \
  list_required_cards, \
  list_required_by_cards, \
  list_random_cards_in_unit, \
  list_all_card_entity_ids

from raw_insert import raw_insert_users, \
  raw_insert_units, \
  raw_insert_cards

from schemas.cards.video_card import schema as video_card_schema
from schemas.cards.choice_card import schema as choice_card_schema

from modules.util import convert_uuid_to_slug


user_a_uuid = uuid.uuid4()
user_b_uuid = uuid.uuid4()
unit_version_a_uuid = uuid.uuid4()
unit_a_uuid = uuid.uuid4()
card_a_uuid = uuid.uuid4()
card_version_a_uuid = uuid.uuid4()
card_b_uuid = uuid.uuid4()
card_version_b_uuid = uuid.uuid4()
test_card_option1_uuid = uuid.uuid4()
test_card_option2_uuid = uuid.uuid4()


def create_card_test_data(db_conn):
  users = [{
    'id': user_a_uuid,
    'name': 'test',
    'email': 'test@example.com',
    'password': 'abcd1234',
  }, {
    'id': user_b_uuid,
    'name': 'other',
    'email': 'other@example.com',
    'password': 'abcd1234',
  }]
  raw_insert_users(db_conn, users)
  units = [{
    'version_id': unit_version_a_uuid,
    'user_id': user_a_uuid,
    'entity_id': unit_a_uuid,
    'name': 'test unit add',
    'body': 'adding numbers is fun'
  }]
  raw_insert_units(db_conn, units)
  cards = [{
    'version_id': card_version_a_uuid,
    'entity_id': card_a_uuid,
    'unit_id': unit_a_uuid,
    'user_id': user_a_uuid,
    'status': 'accepted',
    'kind': 'video',
    'name': 'Meaning of Life Video',
    'data': {
      'site': 'youtube',
      'video_id': convert_uuid_to_slug(uuid.uuid4()),
    },
  }, {
    'version_id': card_version_b_uuid,
    'entity_id': card_b_uuid,
    'unit_id': unit_a_uuid,
    'user_id': user_a_uuid,
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
    'require_ids': [card_a_uuid]
  }]
  raw_insert_cards(db_conn, cards)


def test_get_card_schema(db_conn):
  create_card_test_data(db_conn)
  assert get_card_schema({
    'kind': 'video',
  }) == video_card_schema
  assert get_card_schema({
    'kind': 'choice',
  }) == choice_card_schema


def test_ensure_requires(db_conn):
  create_card_test_data(db_conn)
  data = {
    'require_ids': [card_a_uuid, uuid.uuid4()],
  }
  errors = ensure_requires(db_conn, data)
  assert errors
  data = {
    'require_ids': [card_a_uuid, card_b_uuid],
  }
  errors = ensure_requires(db_conn, data)
  assert not errors


def test_ensure_no_cycles(db_conn):
  create_card_test_data(db_conn)
  data = get_card_version(db_conn, card_version_a_uuid)
  errors = ensure_no_cycles(db_conn, data)
  assert not errors
  data['require_ids'] = [card_b_uuid]
  errors = ensure_no_cycles(db_conn, data)
  assert errors


def test_insert_card(db_conn):
  create_card_test_data(db_conn)
  # A Bad kind
  data = {
    'version_id': uuid.uuid4(),
    'entity_id': uuid.uuid4(),
    'unit_id': unit_a_uuid,
    'user_id': user_a_uuid,
    'status': 'accepted',
    'kind': 'dinosaur',
    'name': 'Story of Love Video',
    'data': {},
  }
  card, errors = insert_card(db_conn, data)
  assert errors
  assert not card
  # A bad require
  data = {
    'version_id': uuid.uuid4(),
    'entity_id': uuid.uuid4(),
    'unit_id': unit_a_uuid,
    'user_id': user_a_uuid,
    'status': 'accepted',
    'kind': 'video',
    'name': 'Story of Love Video',
    'data': {
      'site': 'youtube',
      'video_id': convert_uuid_to_slug(uuid.uuid4()),
    },
    'require_ids': [uuid.uuid4()],
  }
  card, errors = insert_card(db_conn, data)
  assert errors
  assert not card
  # For real
  data = {
    'version_id': uuid.uuid4(),
    'entity_id': uuid.uuid4(),
    'unit_id': unit_a_uuid,
    'user_id': user_a_uuid,
    'status': 'accepted',
    'kind': 'video',
    'name': 'Story of Love Video',
    'data': {
      'site': 'youtube',
      'video_id': convert_uuid_to_slug(uuid.uuid4()),
    },
  }
  card, errors = insert_card(db_conn, data)
  assert not errors
  assert card


def test_insert_card_version(db_conn):
  create_card_test_data(db_conn)
  current_data = get_card_version(db_conn, version_id=card_version_a_uuid)
  # A bad kind
  current_data['kind'] = 'elephant'
  next_data = {
    'user_id': user_b_uuid,
  }
  version, errors = insert_card_version(db_conn, current_data, next_data)
  assert errors
  assert not version
  current_data['kind'] = 'video'
  # A bad require
  next_data = {
    'user_id': user_b_uuid,
    'require_ids': [uuid.uuid4()],
  }
  version, errors = insert_card_version(db_conn, current_data, next_data)
  assert errors
  assert not version
  # For real
  next_data = {
    'user_id': user_b_uuid,
    'name': 'Story of Apathy Video',
    'data': {
      'site': 'youtube',
      'video_id': convert_uuid_to_slug(uuid.uuid4()),
    }
  }
  version, errors = insert_card_version(db_conn, current_data, next_data)
  assert not errors
  assert version


def test_update_card(db_conn):
  create_card_test_data(db_conn)
  current_data = get_card_version(db_conn, version_id=card_version_a_uuid)
  assert current_data['status'] == 'accepted'
  card, errors = update_card(
    db_conn,
    version_id=card_version_a_uuid,
    status='pending'
  )
  assert not errors
  assert card['status'] == 'pending'


def test_validate_card_response(db_conn):
  create_card_test_data(db_conn)
  card = get_card_version(db_conn, version_id=card_version_b_uuid)
  errors = validate_card_response(
    card,
    response=convert_uuid_to_slug(uuid.uuid4())
  )
  assert errors
  errors = validate_card_response(
    card,
    response=convert_uuid_to_slug(test_card_option1_uuid)
  )
  assert not errors


def test_score_card_response(db_conn):
  create_card_test_data(db_conn)
  card = get_card_version(db_conn, version_id=card_version_b_uuid)
  score, feedback = score_card_response(
    card,
    response=convert_uuid_to_slug(test_card_option1_uuid)
  )
  assert score == 1
  score, feedback = score_card_response(
    card,
    response=convert_uuid_to_slug(test_card_option2_uuid)
  )
  assert score == 0
  score, feedback = score_card_response(
    card,
    response=convert_uuid_to_slug(uuid.uuid4())
  )
  assert score == 0
  assert 'Vqjk9WHrR0CSVKQeZZ8svQ' in feedback


def test_deliver_card(db_conn):
  create_card_test_data(db_conn)
  card = get_latest_accepted_card(db_conn, entity_id=card_a_uuid)
  # a bad kind
  card['kind'] = 'eraser'
  assert deliver_card(card, access=None)
  card['kind'] = 'video'
  # for real
  assert deliver_card(card, access=None)
  # access = learn, kind = choice, order = random
  # ... and max_options_to_show < total options
  card = get_latest_accepted_card(db_conn, entity_id=card_b_uuid)
  card['data']['order'] = 'random'
  card['data']['max_options_to_show'] = 1
  result = deliver_card(card, access='learn')
  assert result
  assert result['kind'] == 'choice'
  assert result['data']['options'][0].get('feedback') is None
  assert result['data']['options'][0].get('correct') is None
  assert len(result['data']['options']) == 1


def test_get_latest_accepted_card(db_conn):
  create_card_test_data(db_conn)
  card = get_latest_accepted_card(db_conn, entity_id=card_a_uuid)
  assert card
  assert card['entity_id'] == card_a_uuid


def test_list_latest_accepted_cards(db_conn):
  create_card_test_data(db_conn)
  cards = list_latest_accepted_cards(db_conn, entity_ids=[
    card_a_uuid,
    card_b_uuid,
  ])
  assert cards
  assert len(cards) == 2
  assert cards[0]['entity_id'] in (card_a_uuid,
                                   card_b_uuid,)
  assert cards[1]['entity_id'] in (card_a_uuid,
                                   card_b_uuid,)


def test_list_many_card_versions(db_conn):
  create_card_test_data(db_conn)
  versions = list_many_card_versions(db_conn, version_ids=[
    card_version_a_uuid,
    card_version_b_uuid,
  ])
  assert versions
  assert len(versions) == 2
  assert versions[0]['version_id'] in (card_version_a_uuid,
                                       card_version_b_uuid)
  assert versions[1]['version_id'] in (card_version_a_uuid,
                                       card_version_b_uuid)


def test_get_card_version(db_conn):
  create_card_test_data(db_conn)
  card = get_card_version(db_conn, version_id=card_version_a_uuid)
  assert card


def test_list_one_card_versions(db_conn):
  create_card_test_data(db_conn)
  versions = list_one_card_versions(db_conn, entity_id=card_a_uuid)
  assert versions
  assert len(versions) == 1


def test_list_required_cards(db_conn):
  create_card_test_data(db_conn)
  versions = list_required_cards(db_conn, entity_id=card_b_uuid)
  assert versions
  assert len(versions) == 1
  assert versions[0]['entity_id'] == card_a_uuid


def test_list_required_by_cards(db_conn):
  create_card_test_data(db_conn)
  units = list_required_by_cards(db_conn, entity_id=card_a_uuid)
  assert units
  assert len(units) == 1
  assert units[0]['entity_id'] == card_b_uuid


def test_list_random_cards_in_unit(db_conn):
  create_card_test_data(db_conn)
  cards = list_random_cards_in_unit(db_conn, unit_id=unit_a_uuid, limit=10)
  assert cards
  assert len(cards) == 2


def test_list_all_card_entity_ids(db_conn):
  create_card_test_data(db_conn)
  cards = list_all_card_entity_ids(db_conn)
  assert cards
  assert len(cards) == 2
