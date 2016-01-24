from framework.session import get_current_user
from framework.routes import get, post, abort
from models.card import Card
from models.card_parameters import CardParameters
from models.unit import Unit
from models.set import Set
from models.topic import Topic
from modules.entity import get_card_by_kind
from modules.sequencer.index import update as seq_update
from modules.sequencer.traversal import traverse, judge
from modules.sequencer.card_chooser import choose_card
# from modules.sequencer.params import max_learned


@get('/s/cards/{card_id}')
def get_card_route(request, card_id):
    """
    Get a specific card given an ID. Show all relevant data, but
    not used for the learning interface.
    """

    db_conn = request['db_conn']

    card = get_card_by_kind(db_conn, card_id)
    if not card:
        return abort(404)

    unit = Unit.get_latest_accepted(db_conn, entity_id=card['unit_id'])
    if not unit:
        return abort(404)

    # TODO-2 SPLITUP create new endpoints for these instead
    topics = Topic.list_by_entity_id(db_conn, entity_id=card_id)
    versions = Card.get_versions(db_conn, entity_id=card_id)
    requires = Card.list_requires(db_conn, entity_id=card_id)
    required_by = Card.list_required_by(db_conn, entity_id=card_id)
    params = CardParameters.get(db_conn, entity_id=card_id)

    return 200, {
        'card': card.deliver(access='view'),
        'card_parameters': params.get_values(),
        'unit': unit.deliver(),
        'topics': [topic.deliver() for topic in topics],
        'versions': [version.deliver() for version in versions],
        'requires': [require.deliver() for require in requires],
        'required_by': [require.deliver() for require in required_by],
    }


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

    card = get_card_by_kind(db_conn, card_id)
    if not card:
        return abort(404)

    # Make sure the current unit id matches the card
    context = current_user.get_learning_context()
    if context.get('unit', {}).get('entity_id') != card['unit_id']:
        return abort(400)

    next_ = {
        'method': 'POST',
        'path': '/s/cards/{card_id}/responses'
                .format(card_id=card['entity_id'])
    }
    current_user.set_learning_context(card=card.data, next=next_)

    return 200, {
        'card': card.deliver(access=''),
        'set': context.get('set'),
        'unit': context.get('unit'),
        'next': next_,
    }


@get('/s/cards/{card_id}/versions')
def get_card_versions_route(request, card_id):
    """
    Get versions card given an ID. Paginates.
    """

    db_conn = request['db_conn']
    versions = Card.get_versions(
        db_conn,
        entity_id=card_id,
        **request['params']
    )
    return 200, {
        'versions': [version.deliver(access='view') for version in versions]
    }


@post('/s/cards/{card_id}/responses')
def respond_to_card_route(request, card_id):
    """
    Record and process a learner's response to a card.

    NEXT STATE
    POST Respond Card
        -> GET Learn Card      ...when not ready
        -> GET Choose Unit     ...when ready, but still units
        -> GET View Set Tree   ...when ready and done
    """

    # TODO-3 simplify this method.
    #      perhaps smaller methods or move to model layer?

    db_conn = request['db_conn']
    current_user = get_current_user(request)
    if not current_user:
        return abort(401)

    card = get_card_by_kind(db_conn, card_id)
    if not card:
        return abort(404)

    # Make sure the card is the current one
    context = current_user.get_learning_context()
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

    set_ = Set(context.get('set'))
    unit = Unit(context.get('unit'))

    status = judge(db_conn, unit, current_user)

    # If we are done with this current unit...
    if status == "done":
        buckets = traverse(db_conn, current_user, set_)

        # If there are units to be diagnosed...
        if buckets['diagnose']:
            unit = buckets['diagnose'][0]
            next_card = choose_card(db_conn, current_user, unit)
            next_ = {
                'method': 'GET',
                'path': '/s/cards/{card_id}/learn'
                        .format(card_id=next_card['entity_id']),
            }
            current_user.set_learning_context(
                card=next_card.data, unit=unit.data, next=next_)

        # If there are units to be learned or reviewed...
        elif buckets['learn'] or buckets['review']:
            next_ = {
                'method': 'GET',
                'path': '/s/sets/{set_id}/units'
                        .format(set_id=set_['entity_id']),
            }
            current_user.set_learning_context(card=None, unit=None, next=next_)

        # If we are out of units...
        else:
            next_ = {
                'method': 'GET',
                'path': '/s/sets/{set_id}/tree'
                        .format(set_id=set_['entity_id']),
            }
            current_user.set_learning_context(card=None, unit=None, next=next_)

    # If we are still reviewing, learning or diagnosing this unit...
    else:
        next_card = choose_card(db_conn, current_user, unit)
        if next_card:
            next_ = {
                'method': 'GET',
                'path': '/s/cards/{card_id}/learn'
                        .format(card_id=next_card['entity_id']),
            }
            current_user.set_learning_context(card=next_card.data, next=next_)
        else:
            next_ = {}
            current_user.set_learning_context(next=next_)

    return 200, {
        'response': response.deliver(),
        'feedback': feedback,
        'next': next_,
    }
