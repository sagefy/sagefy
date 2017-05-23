from framework.session import get_current_user
from framework.routes import get, post, abort
from database.topic import list_topics_by_entity_id, deliver_topic
from modules.sequencer.index import update as seq_update
from modules.sequencer.traversal import traverse, judge
from modules.sequencer.card_chooser import choose_card
from database.user import get_learning_context, set_learning_context
from database.response import deliver_response
from database.card_parameters import get_card_parameters, \
    get_card_parameters_values
from database.entity_base import get_latest_accepted, get_versions, \
    list_requires, list_required_by, list_by_entity_ids, get_version
from database.card import deliver_card
from database.unit import deliver_unit

# from modules.sequencer.params import max_learned


@get('/s/cards/{card_id}')
def get_card_route(request, card_id):
    """
    Get a specific card given an ID. Show all relevant data, but
    not used for the learning interface.
    """

    db_conn = request['db_conn']

    card = get_latest_accepted('cards', db_conn, card_id)
    if not card:
        return abort(404)

    unit = get_latest_accepted('units', db_conn, entity_id=card['unit_id'])
    if not unit:
        return abort(404)

    # TODO-2 SPLITUP create new endpoints for these instead
    topics = list_topics_by_entity_id(card_id, {}, db_conn)
    versions = get_versions('cards', db_conn, entity_id=card_id)
    requires = list_requires('cards', db_conn, entity_id=card_id)
    required_by = list_required_by('cards', db_conn, entity_id=card_id)
    params = get_card_parameters({'entity_id': card_id}, db_conn)

    return 200, {
        'card': deliver_card(card, access='view'),
        'card_parameters': (get_card_parameters_values(params)
                            if params else None),
        'unit': deliver_unit(unit),
        'topics': [deliver_topic(topic) for topic in topics],
        'versions': [deliver_card(version) for version in versions],
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
        return abort(404)
    entity_ids = entity_ids.split(',')
    cards = list_by_entity_ids('cards', db_conn, entity_ids)
    if not cards:
        return abort(404)
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
        return abort(401)

    card = get_latest_accepted('cards', db_conn, card_id)
    if not card:
        return abort(404)

    # Make sure the current unit id matches the card
    context = get_learning_context(current_user)
    if context.get('unit', {}).get('entity_id') != card['unit_id']:
        return abort(400)

    next_ = {
        'method': 'POST',
        'path': '/s/cards/{card_id}/responses'
                .format(card_id=card['entity_id'])
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
    versions = get_versions(
        'cards',
        db_conn,
        entity_id=card_id,
        **request['params']
    )
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
    card_version = get_version(db_conn, 'cards', version_id)
    if not card_version:
        return abort(404)
    return 200, {'version': card_version}


@post('/s/cards/{card_id}/responses')
def respond_to_card_route(request, card_id):
    """
    Record and process a learner's response to a card.

    NEXT STATE
    POST Respond Card
        -> GET Learn Card      ...when not ready
        -> GET Choose Unit     ...when ready, but still units
        -> GET View Subject Tree   ...when ready and done
    """

    # TODO-3 simplify this method.
    #      perhaps smaller methods or move to model layer?

    db_conn = request['db_conn']
    current_user = get_current_user(request)
    if not current_user:
        return abort(401)

    card = get_latest_accepted('cards', db_conn, card_id)
    if not card:
        return abort(404)

    # Make sure the card is the current one
    context = get_learning_context(current_user)
    if context.get('card', {}).get('entity_id') != card['entity_id']:
        return abort(400)

    r = seq_update(db_conn, current_user, card,
                   request['params'].get('response'))
    errors, response, feedback = (r.get('errors'), r.get('response'),
                                  r.get('feedback'))
    if errors:
        return 400, {
            'errors': errors,
            'ref': 'wtyOJPoy4bh76OIbYp8mS3LP',
        }

    subject = context.get('subject')
    unit = context.get('unit')

    status = judge(db_conn, unit, current_user)

    # If we are done with this current unit...
    if status == "done":
        buckets = traverse(db_conn, current_user, subject)

        # If there are units to be diagnosed...
        if buckets['diagnose']:
            unit = buckets['diagnose'][0]
            next_card = choose_card(db_conn, current_user, unit)
            next_ = {
                'method': 'GET',
                'path': '/s/cards/{card_id}/learn'
                        .format(card_id=next_card['entity_id']),
            }
            set_learning_context(
                current_user,
                card=next_card.data, unit=unit, next=next_)

        # If there are units to be learned or reviewed...
        elif buckets['learn'] or buckets['review']:
            next_ = {
                'method': 'GET',
                'path': '/s/subjects/{subject_id}/units'
                        .format(subject_id=subject['entity_id']),
            }
            set_learning_context(current_user,
                                 card=None, unit=None, next=next_)

        # If we are out of units...
        else:
            next_ = {
                'method': 'GET',
                'path': '/s/subjects/{subject_id}/tree'
                        .format(subject_id=subject['entity_id']),
            }
            set_learning_context(current_user,
                                 card=None, unit=None, next=next_)

    # If we are still reviewing, learning or diagnosing this unit...
    else:
        next_card = choose_card(db_conn, current_user, unit)
        if next_card:
            next_ = {
                'method': 'GET',
                'path': '/s/cards/{card_id}/learn'
                        .format(card_id=next_card['entity_id']),
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
