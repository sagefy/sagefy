import uuid
from datetime import datetime, timezone
import pytest
from modules.sequencer.traversal import traverse, \
  match_unit_dependents, order_units_by_need, judge
from modules.util import convert_uuid_to_slug
from database.user import get_user
from database.subject import get_latest_accepted_subject
from database.unit import get_latest_accepted_unit, list_latest_accepted_units
from raw_insert import raw_insert_units, raw_insert_cards, \
  raw_insert_responses, raw_insert_subjects
from conftest import user_id

xfail = pytest.mark.xfail

unit_add_uuid = uuid.uuid4()
unit_subtract_uuid = uuid.uuid4()
unit_multiply_uuid = uuid.uuid4()
unit_divide_uuid = uuid.uuid4()
subject_uuid = uuid.uuid4()
card_a_uuid = uuid.uuid4()


def add_test_subject(db_conn):
  """
  Add doesn't require anything.
  Multiply requires add.
  Subtract requires add.
  Divide requires multiply.

  Add is done,
  Subtract needs review,
  Multiply needs to be learned,
  Divide needs to be diagnosed.
  """

  raw_insert_units(db_conn, [{
    'entity_id': unit_add_uuid,
    'user_id': user_id,
    'name': 'Add',
    'body': 'Add',
  }, {
    'entity_id': unit_subtract_uuid,
    'require_ids': [unit_add_uuid],
    'user_id': user_id,
    'name': 'Subtract',
    'body': 'Subtract',
  }, {
    'entity_id': unit_multiply_uuid,
    'require_ids': [unit_add_uuid],
    'user_id': user_id,
    'name': 'Multiply',
    'body': 'Multiply',
  }, {
    'entity_id': unit_divide_uuid,
    'require_ids': [unit_multiply_uuid, unit_subtract_uuid],
    'user_id': user_id,
    'name': 'Divide',
    'body': 'Divide',
  }])

  raw_insert_cards(db_conn, [{
    'entity_id': card_a_uuid,
    'unit_id': unit_add_uuid,
    'user_id': user_id,
    'status': 'accepted',
    'kind': 'video',
    'name': 'Meaning of Life Video',
    'data': {
      'site': 'youtube',
      'video_id': convert_uuid_to_slug(uuid.uuid4()),
    },
  }])

  raw_insert_responses(db_conn, [{
    'user_id': user_id,
    'unit_id': unit_add_uuid,
    'learned': 0.99,
    'card_id': card_a_uuid,
    'response': convert_uuid_to_slug(uuid.uuid4()),
    'score': 1,
  }, {
    'user_id': user_id,
    'unit_id': unit_multiply_uuid,
    'learned': 0.0,
    'card_id': card_a_uuid,
    'response': convert_uuid_to_slug(uuid.uuid4()),
    'score': 1,
  }, {
    'user_id': user_id,
    'unit_id': unit_subtract_uuid,
    'learned': 0.99,
    'card_id': card_a_uuid,
    'response': convert_uuid_to_slug(uuid.uuid4()),
    'score': 1,
    'created': datetime(2004, 11, 3, tzinfo=timezone.utc)
  }])

  raw_insert_subjects(db_conn, [{
    'user_id': user_id,
    'entity_id': subject_uuid,
    'created': datetime(2004, 11, 1, tzinfo=timezone.utc),
    'name': 'Math',
    'body': 'Math',
    'members': [
      {'id': convert_uuid_to_slug(unit_add_uuid), 'kind': 'unit'},
      {'id': convert_uuid_to_slug(unit_subtract_uuid), 'kind': 'unit'},
      {'id': convert_uuid_to_slug(unit_multiply_uuid), 'kind': 'unit'},
      {'id': convert_uuid_to_slug(unit_divide_uuid), 'kind': 'unit'},
    ],
  }])


def test_traverse(db_conn, session):
  """
  Expect to take a list of units and traverse them correctly.
  Basic test.
  """

  add_test_subject(db_conn)
  subject = get_latest_accepted_subject(db_conn, entity_id=subject_uuid)
  assert subject is not None
  user = get_user(db_conn, {'id': user_id})
  buckets = traverse(db_conn, user, subject)
  assert buckets['learn'][0]['entity_id'] in (
    unit_subtract_uuid,
    unit_multiply_uuid,
  )
  assert buckets['learn'][1]['entity_id'] in (
    unit_subtract_uuid,
    unit_multiply_uuid,
  )
  assert buckets['blocked'][0]['entity_id'] == unit_divide_uuid


"""
TODO-3 more traversal tests

traverse
--------
Expect if a node is done, any nodes it requires are left out.
If one node is done, and one is not, continue to the lower node.
Traverse should output units in order.
"""


@xfail
def test_judge_diagnose(db_conn, session):
  """
  Expect to add no known ability to "diagnose".
  """

  add_test_subject(db_conn)
  unit = get_latest_accepted_unit(db_conn, entity_id=unit_divide_uuid)
  user = get_user(db_conn, {'id': user_id})
  assert judge(db_conn, unit, user) == "diagnose"


@xfail
def test_judge_review(db_conn, session):
  """
  Expect to add older, high ability to "review".
  """

  add_test_subject(db_conn)
  unit = get_latest_accepted_unit(db_conn, entity_id=unit_subtract_uuid)
  user = get_user(db_conn, {'id': user_id})
  assert judge(db_conn, unit, user) == "review"


def test_judge_learn(db_conn, session):
  """
  Expect to add known low ability to "learn".
  """

  add_test_subject(db_conn)
  unit = get_latest_accepted_unit(db_conn, entity_id=unit_multiply_uuid)
  user = get_user(db_conn, {'id': user_id})
  assert judge(db_conn, unit, user) == "learn"


def test_judge_done(db_conn, session):
  """
  Expect to show "done".
  """

  add_test_subject(db_conn)
  unit = get_latest_accepted_unit(db_conn, entity_id=unit_add_uuid)
  user = get_user(db_conn, {'id': user_id})
  assert judge(db_conn, unit, user) == "done"


def test_match_unit_dependents(db_conn, session):
  """
  Expect to order units by the number of depending units.
  """

  add_test_subject(db_conn)
  units = list_latest_accepted_units(db_conn, [
    unit_add_uuid,
    unit_subtract_uuid,
    unit_multiply_uuid,
    unit_divide_uuid,
  ])
  deps = match_unit_dependents(units)
  assert len(deps[unit_add_uuid]) == 3
  assert len(deps[unit_multiply_uuid]) == 1
  assert len(deps[unit_subtract_uuid]) == 1
  assert not deps[unit_divide_uuid]


def test_order(db_conn, session):
  """
  Expect to order units by the number of depending units.
  """

  add_test_subject(db_conn)
  units = list_latest_accepted_units(db_conn, [
    unit_add_uuid,
    unit_subtract_uuid,
    unit_multiply_uuid,
    unit_divide_uuid,
  ])
  units = order_units_by_need(units)
  entity_ids = [unit['entity_id'] for unit in units]
  assert entity_ids[0] == unit_add_uuid
  assert entity_ids[1] in (unit_subtract_uuid, unit_multiply_uuid)
  assert entity_ids[2] in (unit_subtract_uuid, unit_multiply_uuid)
  assert entity_ids[3] == unit_divide_uuid
