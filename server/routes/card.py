from copy import deepcopy

from framework.session import get_current_user
from framework.routes import get, post, abort
from modules.util import convert_uuid_to_slug
from modules.sequencer.index import update as seq_update
from modules.sequencer.traversal import traverse, judge
from modules.sequencer.card_chooser import choose_card
from database.user import get_learning_context, set_learning_context
from database.response import deliver_response
from database.card_parameters import get_card_parameters, \
    get_card_parameters_values
from database.card import deliver_card, insert_card, get_latest_accepted_card
from database.unit import deliver_unit, get_latest_accepted_unit
from database.card import list_required_cards, list_required_by_cards, \
    list_latest_accepted_cards, list_one_card_versions, get_card_version, \
    insert_card_version


# from modules.sequencer.params import max_learned


@get('/s/cards/{card_id}')
def get_card_route(request, card_id):
  """
  Get a specific card given an ID. Show all relevant data, but
  not used for the learning interface.
  """

  db_conn = request['db_conn']
  card = get_latest_accepted_card(db_conn, card_id)
  if not card:
    return abort(404, 'fPebfwqfRNmOiSWqWISeaA')
  unit = get_latest_accepted_unit(db_conn, card['unit_id'])
  if not unit:
    return abort(404, 'IKSqfvHvRK6hbSAIOkQuLg')
  # TODO-2 SPLITUP create new endpoints for these instead
  requires = list_required_cards(db_conn, card_id)
  required_by = list_required_by_cards(db_conn, card_id)
  params = get_card_parameters(db_conn, {'entity_id': card_id})
  return 200, {
    'card': deliver_card(card, access='view'),
    'card_parameters': (get_card_parameters_values(params)
                        if params else None),
    'unit': deliver_unit(unit),
    'requires': [deliver_card(require) for require in requires],
    'required_by': [deliver_card(require) for require in required_by],
  }


@get('/s/cards')
def list_cards_route(request):
  """
  Return a collection of cards by `entity_id`.
  """

  db_conn = request['db_conn']
  entity_ids = request['params'].get('entity_ids')
  if not entity_ids:
    return abort(404, 'ESKDY5E7QA6tIpAv9i6WMw')
  entity_ids = entity_ids.split(',')
  cards = list_latest_accepted_cards(db_conn, entity_ids)
  if not cards:
    return abort(404, 's0uGKuNDSJK00pJs-x1AAQ')
  return 200, {'cards': [deliver_card(card, 'view') for card in cards]}


@get('/s/cards/{card_id}/learn')  # TODO-3 merge with main GET route
def learn_card_route(request, card_id):
  """
  Render the card's data, ready for learning.

  NEXT STATE
  GET Learn Card
    -> POST Respond Card
  """

  db_conn = request['db_conn']
  current_user = get_current_user(request)
  if not current_user:
    return abort(401, 'WBv3UeikTLu5AAwG9A0QZg')
  card = get_latest_accepted_card(db_conn, card_id)
  if not card:
    return abort(404, 'UgQHXzx4SSaHgJzHpRaL9g')
  # Make sure the current unit id matches the card
  context = get_learning_context(current_user)
  context_unit_id = context.get('unit', {}).get('entity_id')
  if context_unit_id != convert_uuid_to_slug(card['unit_id']):
    return 400, {
      'errors': [{
        'name': 'unit_id',
        'message': 'card not in current unit.',
        'ref': 'd6rhaoCuRdW0f9j8AlMXBQ',
      }],
    }
  next_ = {
    'method': 'POST',
    'path': '/s/cards/{card_id}/responses'.format(
      card_id=convert_uuid_to_slug(card['entity_id'])
    )
  }
  set_learning_context(current_user, card=card, next=next_)
  return 200, {
    'card': deliver_card(card, access='learn'),
    'subject': context.get('subject'),
    'unit': context.get('unit'),
    'next': next_,
  }


@get('/s/cards/{card_id}/versions')
def get_card_versions_route(request, card_id):
  """
  Get versions card given an ID. Paginates.
  """

  db_conn = request['db_conn']
  versions = list_one_card_versions(db_conn, card_id)
  return 200, {
    'versions': [
      deliver_card(version, access='view')
      for version in versions
    ]
  }


@get('/s/cards/versions/{version_id}')
def get_card_version_route(request, version_id):
  """
  Get a card version only knowing the `version_id`.
  """

  db_conn = request['db_conn']
  card_version = get_card_version(db_conn, version_id)
  if not card_version:
    return abort(404, 'n0Pl_2mnSxydg0sUeu6H4A')
  return 200, {'version': card_version}


@post('/s/cards/{card_id}/responses')
def respond_to_card_route(request, card_id):
  """
  Record and process a learner's response to a card.

  NEXT STATE
  POST Respond Card
    -> GET Learn Card    ...when not ready
    -> GET Choose Unit   ...when ready, but still units
    -> GET View Subject Tree   ...when ready and done
  """

  # TODO-3 simplify this method.
  #    perhaps smaller methods or move to model layer?
  db_conn = request['db_conn']
  current_user = get_current_user(request)
  if not current_user:
    return abort(401, 'XDVEHHLRSZqQNJW4Zi_iqw')
  card = get_latest_accepted_card(db_conn, card_id)
  if not card:
    return abort(404, 'TQZ3SmAhS1qBd274C9DG0w')
  # Make sure the card is the current one
  context = get_learning_context(current_user)
  context_card_id = context.get('card', {}).get('entity_id')
  if context_card_id != convert_uuid_to_slug(card['entity_id']):
    return 400, {
      'errors': [{
        'message': 'Not the current card.',
        'ref': 'XfmF52NmQnK_bbaxx-p8dg',
      }]
    }
  result = seq_update(db_conn, current_user, card,
                      request['params'].get('response'))
  errors, response, feedback = (result.get('errors'), result.get('response'),
                                result.get('feedback'))
  if errors:
    return 400, {
      'errors': errors,
      'ref': 'HfuW7_B-TByy8yh4FwgdrA',
    }

  subject = context.get('subject')
  unit = context.get('unit')

  status = judge(db_conn, unit, current_user)

  # If we are done with this current unit...
  if status == "done":
    buckets = traverse(db_conn, current_user, subject)

    # If there are units to be diagnosed...
    if buckets.get('diagnose'):
      unit = buckets['diagnose'][0]
      next_card = choose_card(db_conn, current_user, unit)
      next_ = {
        'method': 'GET',
        'path': '/s/cards/{card_id}/learn'.format(
          card_id=convert_uuid_to_slug(next_card['entity_id'])
        ),
      }
      set_learning_context(
        current_user,
        card=next_card.data,
        unit=unit,
        next=next_
      )

    # If there are units to be learned or reviewed...
    elif buckets.get('learn') or buckets.get('review'):
      next_ = {
        'method': 'GET',
        'path': '/s/subjects/{subject_id}/units'.format(
          subject_id=convert_uuid_to_slug(subject['entity_id'])
        ),
      }
      set_learning_context(current_user,
                           card=None, unit=None, next=next_)

    # If we are out of units...
    else:
      next_ = {
        'method': 'GET',
        'path': '/s/subjects/{subject_id}/tree'.format(
          subject_id=convert_uuid_to_slug(subject['entity_id'])
        ),
      }
      set_learning_context(current_user,
                           card=None, unit=None, next=next_)

  # If we are still reviewing, learning or diagnosing this unit...
  else:
    next_card = choose_card(db_conn, current_user, unit)
    if next_card:
      next_ = {
        'method': 'GET',
        'path': '/s/cards/{card_id}/learn'.format(
          card_id=convert_uuid_to_slug(next_card['entity_id'])
        ),
      }
      set_learning_context(current_user, card=next_card, next=next_)
    else:
      next_ = {}
      set_learning_context(current_user, next=next_)

  return 200, {
    'response': deliver_response(response),
    'feedback': feedback,
    'next': next_,
  }


@post('/s/cards/versions')
def create_new_card_version_route(request):
  """
  Create a new card version for a brand new card.
  """

  current_user = get_current_user(request)
  if not current_user:
    return abort(401, '_YQNk1foSXyDwrnuxnThNw')
  db_conn = request['db_conn']
  data = deepcopy(request['params'])
  if 'entity_id' in data:
    return abort(403, 'sdXoDQ-tRweCUg35MUcUEA')
  data['user_id'] = current_user['id']
  card, errors = insert_card(db_conn, data)
  if errors:
    return 400, {
      'errors': errors,
      'ref': '8X-cJFZPQIyyAJJWmfiS7A',
    }
  return 200, {'version': deliver_card(card, 'view')}


@post('/s/cards/{card_id}/versions')
def create_existing_card_version_route(request, card_id):
  """
  Create a new card version for an existing card.
  """

  current_user = get_current_user(request)
  if not current_user:
    return abort(401, 'a3vXGVFCRpWwf8WEkqtBgQ')
  db_conn = request['db_conn']
  next_data = deepcopy(request['params'])
  next_data['entity_id'] = card_id
  next_data['user_id'] = current_user['id']
  current_data = get_latest_accepted_card(db_conn, card_id)
  if not current_data:
    return abort(404, 'dQvoI_OjQY2U-GeyP8fsTA')
  card, errors = insert_card_version(db_conn, current_data, next_data)
  if errors:
    return 400, {
      'errors': errors,
      'ref': 'DyKLB28gT6CYGdyQ9smOKQ',
    }
  return 200, {'version': deliver_card(card, 'view')}
