from framework.routes import get, post, put, delete, abort
from framework.session import get_current_user
from database.user import set_learning_context, get_user
from database.user_subjects import insert_user_subject, list_user_subjects, \
    remove_user_subject, list_user_subjects_entity
from database.subject import deliver_subject, get_latest_accepted_subject
from modules.sequencer.traversal import traverse
from modules.util import convert_slug_to_uuid, convert_uuid_to_slug


@get('/s/users/{user_id}/subjects')
def list_user_subjects_route(request, user_id):
  """
  Get the list of subjects the user has added.

  NEXT STATE
  GET Choose Subject
    -> POST Choose Subject
  """

  db_conn = request['db_conn']
  current_user = get_current_user(request)
  # Get the user in question
  if current_user and current_user['id'] == convert_slug_to_uuid(user_id):
    user = current_user
  else:
    user = get_user(db_conn, {'id': user_id})
    if not user:
      return abort(404, 'MhNh85CERQe6Zgv-qRO6Zg')
    if user['settings']['view_subjects'] != 'public':
      return abort(403, 'TcKwVsp9Q6WAkJSV-QKuSQ')
  params = request['params']
  user_subjects = list_user_subjects_entity(db_conn, user_id, params)
  response = {
    'subjects': [
      deliver_subject(subject)
      for subject in user_subjects
    ]
  }
  if current_user == user:
    next_ = {
      'method': 'POST',
      'path': '/s/users/{user_id}/subjects/{subject_id}'.format(
        user_id=current_user['id'],
        subject_id='{subject_id}'
      ),
    }
    set_learning_context(current_user, next=next_)
    response['next'] = next_
  return 200, response


@post('/s/users/{user_id}/subjects/{subject_id}')
def add_subject_route(request, user_id, subject_id):
  """
  Add a subject to the learner's list of subjects.
  """

  db_conn = request['db_conn']
  current_user = get_current_user(request)
  if not current_user:
    return abort(401, 'FOcE-QweTEuronDPd6lIyQ')
  if convert_slug_to_uuid(user_id) != current_user['id']:
    return abort(403, 'CoCLK9yUQ0O8fA4S4vS_HQ')
  subject = get_latest_accepted_subject(db_conn, subject_id)
  if not subject:
    return abort(404, 'm8rffEXsQGSmKbO2ee1Zkg')
  # TODO-1 handle if subject already added
  user_subject, errors = insert_user_subject(db_conn, user_id, subject_id)
  if errors:
    return 400, {
      'errors': errors,
      'ref': 'hL92UUGXQk6OhOggTZzarA'
    }
  return 200, {'user_subject': user_subject}


@put('/s/users/{user_id}/subjects/{subject_id}')
def select_subject_route(request, user_id, subject_id):
  """
  Select the subject to work on.

  NEXT STATE
  POST Choose Subject   (Update Learner Context)
    -> GET Choose Subject ...when subject is complete
    -> GET Choose Unit  ...when in learn or review mode
    -> GET Learn Card   ...when in diagnosis
      (Unit auto chosen)
  """

  db_conn = request['db_conn']
  current_user = get_current_user(request)
  if not current_user:
    return abort(401, 'f8IynoM9RLmW0Ae14_Hukw')
  subject = get_latest_accepted_subject(db_conn, subject_id)
  set_learning_context(current_user, subject=subject)
  buckets = traverse(db_conn, current_user, subject)
  # When in diagnosis, choose the unit and card automagically.
  # if buckets.get('diagnose'):
  #   unit = buckets['diagnose'][0]
  #   card = choose_card(db_conn, current_user, unit)
  #   next_ = {
  #     'method': 'GET',
  #     'path': '/s/cards/{card_id}/learn'
  #         .format(card_id=convert_uuid_to_slug(card['entity_id'])),
  #   }
  #   set_learning_context(
  #     current_user,
  #     next=next_, unit=unit, card=card)
  # When in learn or review mode, lead me to choose a unit.
  # elif buckets.get('review') or
  if buckets.get('learn'):
    next_ = {
      'method': 'GET',
      'path': '/s/subjects/{subject_id}/units'.format(
        subject_id=convert_uuid_to_slug(subject_id)
      ),
    }
    set_learning_context(current_user, next=next_)
  # If the subject is complete, lead the learner to choose another subject.
  else:
    next_ = {
      'method': 'GET',
      'path': '/s/users/{user_id}/subjects'.format(
        user_id=convert_uuid_to_slug(current_user['id'])
      ),
    }
    set_learning_context(current_user, next=next_, unit=None, subject=None)
  return 200, {'next': next_}


@delete('/s/users/{user_id}/subjects/{subject_id}')
def remove_subject_route(request, user_id, subject_id):
  """
  Remove a subject from the learner's list of subjects.
  """

  db_conn = request['db_conn']
  current_user = get_current_user(request)
  if not current_user:
    return abort(401, 'DHlX2XTsTO-1Hhfr9GXkJw')
  if user_id != current_user['id']:
    return abort(403, '8yt2d8K1RNKidGIVU1CaOA')
  user_subjects = list_user_subjects(db_conn, user_id)
  if not user_subjects:
    return 404, {
      'errors': [{
        'name': 'user_id',
        'message': 'User does not have subjects.',
        'ref': 'nttevgwMRsOwiT_ul0SmHQ',
      }],
    }
  matches = [
    us
    for us in user_subjects
    if (convert_slug_to_uuid(us['subject_id']) ==
        convert_slug_to_uuid(subject_id))
  ]
  if not matches:
    return abort(404, 'AQV0c9qfSdO7Ql2IC8l0bw')
  errors = remove_user_subject(db_conn, user_id, subject_id)
  if errors:
    return 400, {
      'errors': errors,
      'ref': 'h1BKySSTT0SgH2OTTnSVlA'
    }
  return 200, {}
