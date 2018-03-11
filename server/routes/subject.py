from copy import deepcopy
from framework.routes import get, post, abort
from framework.session import get_current_user
from modules.sequencer.traversal import traverse, judge
from modules.sequencer.card_chooser import choose_card
from modules.util import convert_uuid_to_slug
from database.user import get_learning_context, set_learning_context
from database.subject import deliver_subject, insert_subject, \
    get_latest_accepted_subject
from database.entity_facade import list_subjects_by_unit_recursive
from database.unit import deliver_unit, get_latest_accepted_unit
from database.entity_facade import list_units_in_subject_recursive
from database.subject import list_latest_accepted_subjects, \
    list_one_subject_versions, get_subject_version, insert_subject_version, \
    get_recommended_subjects, list_my_recently_created_subjects


@get('/s/subjects/recommended')
def get_recommended_subjects_route(request):
  db_conn = request['db_conn']
  subjects = get_recommended_subjects(db_conn)
  if not subjects:
    return abort(404, '44bN2oD3TuOWc8wrgRmeeA')
  return 200, {
    'subjects': [deliver_subject(subject) for subject in subjects]
  }


@get('/s/subjects/{subject_id}')
def get_subject_route(request, subject_id):
  """
  Get a specific subject given an ID.
  """

  db_conn = request['db_conn']
  subject = get_latest_accepted_subject(db_conn, subject_id)
  if not subject:
    return abort(404, 'pY3NrIXFTuaxy2F0dnf7Cg')
  # TODO-2 SPLITUP create new endpoints for these instead
  units = list_units_in_subject_recursive(db_conn, subject)
  return 200, {
    'subject': deliver_subject(subject),
    # TODO-3 subject parameters
    'units': [deliver_unit(unit) for unit in units],
  }


@get('/s/subjects')
def list_subjects_route(request):
  """
  Return a collection of subjects by `entity_id`.
  """

  db_conn = request['db_conn']
  entity_ids = request['params'].get('entity_ids')
  if not entity_ids:
    return abort(404, 'COhZEG0GTW6L2bPh6AYsfw')
  entity_ids = entity_ids.split(',')
  subjects = list_latest_accepted_subjects(db_conn, entity_ids)
  if not subjects:
    return abort(404, 'ZlLFtBwdS-Sj49ASUoGPZw')
  return 200, {
    'subjects': [deliver_subject(subject, 'view') for subject in subjects]
  }


@get('/s/subjects/{subject_id}/versions')
def get_subject_versions_route(request, subject_id):
  """
  Get subject versions given an ID. Paginates.
  """

  db_conn = request['db_conn']
  versions = list_one_subject_versions(db_conn, subject_id)
  return 200, {
    'versions': [
      deliver_subject(version, access='view')
      for version in versions
    ]
  }


@get('/s/subjects/versions/{version_id}')
def get_subject_version_route(request, version_id):
  """
  Get a subject version only knowing the `version_id`.
  """

  db_conn = request['db_conn']
  subject_version = get_subject_version(db_conn, version_id)
  if not subject_version:
    return abort(404, 'w4tZ5D0iRNmfwNTaD-sXzQ')
  return 200, {'version': subject_version}


@get('/s/subjects/{subject_id}/tree')
def get_subject_tree_route(request, subject_id):
  """
  Render the tree of units that exists within a subject.

  Contexts:
  - Search subject, preview units in subject
  - Pre diagnosis
  - Learner view progress in subject
  - Subject complete

  TODO-2 merge with get_subject_units_route
  TODO-2 simplify this method
  """

  db_conn = request['db_conn']
  subject = get_latest_accepted_subject(db_conn, subject_id)
  if not subject:
    return abort(404, '66ejBlFdQ4aYy5MBuP501Q')
  units = list_units_in_subject_recursive(db_conn, subject)
  # For the menu, it must return the name and ID of the subject
  output = {
    'subjects': deliver_subject(subject),
    'units': [deliver_unit(unit) for unit in units],
  }
  current_user = get_current_user(request)
  if not current_user:
    return 200, output
  buckets = traverse(db_conn, current_user, subject)
  output['buckets'] = {
    # 'diagnose': [u['entity_id'] for u in buckets['diagnose']],
    # 'review': [u['entity_id'] for u in buckets['review']],
    'blocked': [u['entity_id'] for u in buckets['blocked']],
    'learn': [u['entity_id'] for u in buckets['learn']],
    'done': [u['entity_id'] for u in buckets['done']],
  }
  return 200, output


@get('/s/subjects/{subject_id}/units')
def get_subject_units_route(request, subject_id):
  """
  Present a small number of units the learner can choose from.

  NEXT STATE
  GET Choose Unit
    -> POST Choose Unit
  """

  db_conn = request['db_conn']
  # TODO-3 simplify this method. should it be part of the models?
  current_user = get_current_user(request)
  if not current_user:
    return abort(401, 'p_wleq0FRQ2HEuHKOJIb7Q')
  context = get_learning_context(current_user)
  next_ = {
    'method': 'POST',
    'path': '/s/subjects/{subject_id}/units/{unit_id}'.format(
      subject_id=context.get('subject', {}).get('entity_id'),
      unit_id='{unit_id}'
    ),
  }
  set_learning_context(current_user, next=next_)
  subject = get_latest_accepted_subject(db_conn, subject_id)
  if not subject:
    return abort(404, '68VOXmd6Shq2cwAAktkFtw')
  # Pull a list of up to 5 units to choose from based on priority.
  buckets = traverse(db_conn, current_user, subject)
  units = buckets['learn'][:5]
  # TODO-3 Time estimates per unit for mastery.
  return 200, {
    'next': next_,
    'units': [deliver_unit(unit) for unit in units],
    # For the menu, it must return the name and ID of the subject
    'subject': deliver_subject(subject),
    'current_unit_id': context.get('unit', {}).get('entity_id'),
  }


@post('/s/subjects/{subject_id}/units/{unit_id}')
def choose_unit_route(request, subject_id, unit_id):
  """
  Updates the learner's information based on the unit they have chosen.

  NEXT STATE
  POST Chosen Unit
    -> GET Learn Card
  """

  # TODO-3 simplify this method. should it be broken up or moved to model?
  db_conn = request['db_conn']
  current_user = get_current_user(request)
  if not current_user:
    return abort(401, 'NcrRkqIlSW-BkcWLBkwORQ')
  unit = get_latest_accepted_unit(db_conn, unit_id)
  if not unit:
    return abort(404, 'PIti_qwAQ7WXwQwNZertxw')
  # If the unit isn't in the subject...
  context = get_learning_context(current_user)
  subject_ids = [
    convert_uuid_to_slug(subject['entity_id'])
    for subject in list_subjects_by_unit_recursive(db_conn, unit_id)
  ]
  context_subject_id = context.get('subject', {}).get('entity_id')
  if context_subject_id not in subject_ids:
    return 400, {
      'errors': [{
        'message': 'Unit not in subject.',
        'ref': 'r32fH0eCRZCivJoh-hKwZQ',
      }]
    }
  # Or, the unit doesn't need to be learned...
  status = judge(db_conn, unit, current_user)
  if status == "done":
    return 400, {
      'errors': [{
        'message': 'Unit not needed.',
        'ref': 'YTU27E63Rfiy3Rqmqd6Bew',
      }]
    }
  # Choose a card for the learner to learn
  card = choose_card(db_conn, current_user, unit)
  if card:
    next_ = {
      'method': 'GET',
      'path': '/s/cards/{card_id}/learn'.format(
        card_id=convert_uuid_to_slug(card['entity_id'])
      ),
    }
  else:
    next_ = {}
  set_learning_context(
    current_user,
    unit=unit,
    card=card if card else None,
    next=next_
  )
  return 200, {'next': next_}


# TODO-1 move to /s/users/{user_id}/subjects (?)
@get('/s/subjects:get_my_recently_created')
def get_my_recently_created_subjects_route(request):
  """
  Get the subjects the user most recently created.
  """

  current_user = get_current_user(request)
  if not current_user:
    return abort(401, 'MEnwdloNQLWEVnZNT1YRFg')
  db_conn = request['db_conn']
  subjects = list_my_recently_created_subjects(db_conn, current_user['id'])
  return 200, {
    'subjects': [deliver_subject(subject) for subject in subjects],
  }


@post('/s/subjects/versions')
def create_new_subject_version_route(request):
  """
  Create a new subject version for a brand new subject.
  """

  current_user = get_current_user(request)
  if not current_user:
    return abort(401, 'TFsImo88TtuYyfYPq4eDwg')
  db_conn = request['db_conn']
  data = deepcopy(request['params'])
  if 'entity_id' in data:
    return abort(403, 'HoZHBw0kTfe87HgWZZJ2tg')
  data['user_id'] = current_user['id']
  subject, errors = insert_subject(db_conn, data)
  if errors:
    return 400, {
      'errors': errors,
      'ref': 'niK3wz6xQn-0pDUzK1T59w',
    }
  return 200, {'version': deliver_subject(subject, 'view')}


@post('/s/subjects/{subject_id}/versions')
def create_existing_subject_version_route(request, subject_id):
  """
  Create a new subject version for an existing subject.
  """

  current_user = get_current_user(request)
  if not current_user:
    return abort(401, 'h5Y9A96sThqLJV-4tMuf3A')
  db_conn = request['db_conn']
  next_data = deepcopy(request['params'])
  next_data['entity_id'] = subject_id
  next_data['user_id'] = current_user['id']
  current_data = get_latest_accepted_subject(db_conn, subject_id)
  if not current_data:
    return abort(404, '4upY7gTvQWSKJwgi0rhBQg')
  subject, errors = insert_subject_version(db_conn, current_data, next_data)
  if errors:
    return 400, {
      'errors': errors,
      'ref': 'QYUbgqfTQk2dXMmOC4DBSA',
    }
  return 200, {'version': deliver_subject(subject, 'view')}
