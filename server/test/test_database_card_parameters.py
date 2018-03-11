
from database.card_parameters import get_card_parameters, \
  insert_card_parameters, \
  update_card_parameters, \
  get_distribution, \
  deliver_distribution, \
  bundle_distribution, \
  get_guess, \
  get_slip, \
  get_transit, \
  get_num_learners, \
  get_card_parameters_values
from database.card import get_latest_accepted_card
from test_database_card import create_card_test_data, card_a_uuid, card_b_uuid


def test_get_card_parameters(db_conn):
  create_card_test_data(db_conn)
  params = {
    'entity_id': card_b_uuid,
  }
  card_params = get_card_parameters(db_conn, params)
  assert card_params


def test_insert_card_parameters(db_conn):
  create_card_test_data(db_conn)
  data = {
    'entity_id': card_a_uuid,
    'guess_distribution': {},
    'slip_distribution': {},
  }
  cp, errors = insert_card_parameters(db_conn, data)
  assert not errors
  assert cp


def test_update_card_parameters(db_conn):
  create_card_test_data(db_conn)
  prev_data = get_latest_accepted_card(db_conn, entity_id=card_b_uuid)
  data = {
    'guess_distribution': {},
    'slip_distribution': {},
  }
  cp, errors = update_card_parameters(db_conn, prev_data, data)
  assert not errors
  assert cp


def test_get_distribution(db_conn):
  create_card_test_data(db_conn)
  params = {
    'entity_id': card_b_uuid,
  }
  card_params = get_card_parameters(db_conn, params)
  dist = get_distribution(card_params, kind='guess')
  assert dist
  params = {
    'entity_id': card_a_uuid,
  }
  card_params = get_card_parameters(db_conn, params) or {}
  dist = get_distribution(card_params, kind='slip')
  assert dist


def test_deliver_distribution():
  hypotheses = {'1': 0}
  result = deliver_distribution(hypotheses)
  assert 1 in result


def test_bundle_distribution():
  hypotheses = {1: 0}
  result = bundle_distribution(hypotheses)
  assert '1' in result


def test_get_guess(db_conn):
  create_card_test_data(db_conn)
  params = {
    'entity_id': card_b_uuid,
  }
  card_params = get_card_parameters(db_conn, params)
  assert get_guess(card_params) == 0.41


def test_get_slip(db_conn):
  create_card_test_data(db_conn)
  params = {
    'entity_id': card_b_uuid,
  }
  card_params = get_card_parameters(db_conn, params)
  assert 0.27 < get_slip(card_params) < 0.28


def test_get_transit():
  assert get_transit() == 0.05


def test_get_num_learners():
  assert get_num_learners() == 0


def test_get_card_parameters_values(db_conn):
  create_card_test_data(db_conn)
  params = {
    'entity_id': card_b_uuid,
  }
  card_params = get_card_parameters(db_conn, params)
  result = get_card_parameters_values(card_params)
  assert 'guess' in result
  assert 'slip' in result
  assert 'transit' in result
  assert 'num_learners' in result
