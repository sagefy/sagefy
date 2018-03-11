from modules.memoize_redis import memoize_redis
from database.user import get_user
from database.card import get_card_version, list_latest_accepted_cards, \
  update_card, list_one_card_versions
from database.subject import list_subjects_by_unit_flat, \
  list_subject_parents, list_latest_accepted_subjects, \
  get_subject_version, update_subject, list_one_subject_versions
from database.unit import list_latest_accepted_units, \
  update_unit, get_unit_version, list_one_unit_versions


def get_entity_version(db_conn, kind, version_id):
  """

  """

  assert kind in ('card', 'unit', 'subject')
  if kind == 'card':
    return get_card_version(db_conn, version_id)
  if kind == 'unit':
    return get_unit_version(db_conn, version_id)
  if kind == 'subject':
    return get_subject_version(db_conn, version_id)


def list_one_entity_versions(db_conn, kind, entity_id):
  """

  """

  assert kind in ('card', 'unit', 'subject')
  if kind == 'card':
    return list_one_card_versions(db_conn, entity_id)
  if kind == 'unit':
    return list_one_unit_versions(db_conn, entity_id)
  if kind == 'subject':
    return list_one_subject_versions(db_conn, entity_id)


def update_entity_status_by_kind(db_conn, kind, version_id, status):
  """

  """

  assert kind in ('card', 'unit', 'subject')
  if kind == 'card':
    return update_card(db_conn, version_id, status)
  if kind == 'unit':
    return update_unit(db_conn, version_id, status)
  if kind == 'subject':
    return update_subject(db_conn, version_id, status)


def list_subjects_by_unit_recursive(db_conn, unit_id):
  """
  Get a list of subjects which contain the given member ID. Recursive.
  TODO-2 is there a way to simplify this method?
  """

  def _():
    # *** First, find the list of subjects
    #   directly containing the member ID. ***
    subjects = list_subjects_by_unit_flat(db_conn, unit_id)

    # *** Second, find all the subjects containing
    #   those subjects... recursively. ***
    found_subjects, all_subjects = subjects, []
    while found_subjects:
      all_subjects += found_subjects
      subject_ids = {
        subject['entity_id']
        for subject in found_subjects
      }
      found_subjects = []
      for subject_id in subject_ids:
        found_subjects += list_subject_parents(db_conn, subject_id)
    return all_subjects

  key = 'list_subjects_by_unit_{id}'.format(id=unit_id)
  return [data for data in memoize_redis(key, _)]


def list_units_in_subject_recursive(db_conn, main_subject):
  """
  Get the list of units contained within the subject.
  Recursive. Connecting.
  TODO-2 what about required units outside the subject?
  """

  def _():
    # *** First, we need to break down
    #   the subject into a list of known units. ***
    unit_ids = set()
    subjects = [main_subject]
    while subjects:
      subject_ids = set()
      for subject in subjects:
        unit_ids.update({
          member['id']
          for member in subject.get('members')
          if member['kind'] == 'unit'
        })
        subject_ids.update({
          member['id']
          for member in subject.get('members')
          if member['kind'] == 'subject'
        })
      subjects = list_latest_accepted_subjects(db_conn, subject_ids)

    # *** Second, we need to find all
    #   the required connecting units. ***
    units = list_latest_accepted_units(db_conn, unit_ids)
    return units

  # If we already have it stored, use that
  key = 'subject_{id}'.format(id=main_subject['entity_id'])
  return [data for data in memoize_redis(key, _)]


def find_requires_cycle(db_conn, tablename, data):
  """
  Inspect own requires to see if a cycle is formed.
  """

  assert tablename in ('cards', 'units')
  seen = set()
  main_id = data['entity_id']
  found = {'cycle': False}

  def _(require_ids):
    if tablename == 'cards':
      entities = list_latest_accepted_cards(db_conn, require_ids)
    elif tablename == 'units':
      entities = list_latest_accepted_units(db_conn, require_ids)
    for entity in entities:
      if entity['entity_id'] == main_id:
        found['cycle'] = True
        break
      if entity['entity_id'] not in seen:
        seen.add(entity['entity_id'])
        if 'require_ids' in entity:
          _(entity['require_ids'])

  _(data['require_ids'])
  return found['cycle']


def get_entity_status(current_status, votes):
  """
  Returns (changed, status) ... one of:
  (True, 'accepted|blocked|pending')
  (False, 'accepted|blocked|pending|declined')

  TODO-2 Update this to work as described in:
    http://docs.sagefy.org/Planning-Contributor-Ratings
    This requires knowing two things:
    - Number of learners the entity impacts
    - The vote and proposal history of the contributor
  """

  # Make sure the entity version status is not declined or accepted
  if current_status in ('accepted', 'declined'):
    return False, current_status
  # TODO-3 for now, we'll just accept all proposals as is
  # The algorithm should eventually be updated to match
  # https://docs.sagefy.org/Planning-Contributor-Ratings
  return True, 'accepted'


def update_entity_statuses(db_conn, proposal):
  """
  Update the entity's status based on the vote power received.
  Move to accepted or blocked if qualified.
  """

  from database.post import list_votes_by_proposal
  from modules.notices import send_notices

  for eev in proposal['entity_versions']:
    entity_kind, version_id = eev['kind'], eev['id']
    entity_version = get_entity_version(db_conn, entity_kind, version_id)
    votes = list_votes_by_proposal(db_conn, proposal['id'])
    changed, status = get_entity_status(entity_version['status'], votes)
    if changed:
      entity_version['status'] = status
      user = get_user(db_conn, {'id': proposal['user_id']})
      update_entity_status_by_kind(
        db_conn,
        kind=entity_kind,
        version_id=version_id,
        status=status
      )
      send_notices(
        db_conn,
        entity_id=version_id,
        entity_kind=entity_kind,
        notice_kind=('block_proposal'
                     if status == 'blocked' else
                     'accept_proposal'),
        notice_data={
          'user_name': user['name'],
          'proposal_name': proposal['body'],
          'entity_kind': entity_kind,
          'entity_name': entity_version['name'],
        }
      )
