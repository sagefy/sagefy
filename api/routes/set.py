from framework.routes import get, post, abort
from models.set import Set
from models.topic import Topic
from models.unit import Unit
from framework.session import get_current_user

# Nota Bene: We use `set_` because `set` is a type in Python


@get('/api/sets/{set_id}')
def get_set_route(request, set_id):
    """
    Get a specific set given an ID.
    """

    set_ = Set.get_latest_accepted(set_id)
    if not set_:
        return abort(404)

    topics = Topic.list_by_entity_id(entity_id=set_id)
    versions = Set.get_versions(entity_id=set_id)
    units = set_.list_units()

    return 200, {
        'set': set_.deliver(),
        'topics': [topic.deliver() for topic in topics],
        'versions': [version.deliver() for version in versions],
        'units': [unit.deliver() for unit in units],
    }

    # TODO@ sequencer: learners, quality, difficulty


@get('/api/sets/{set_id}/versions')
def get_set_versions_route(request, set_id):
    """
    Get versions set given an ID. Paginates.
    """

    versions = Set.get_versions(entity_id=set_id, **request['params'])
    return 200, {
        'versions': [version.deliver(access='view') for version in versions]
    }


@get('/api/sets/{set_id}/tree')
def get_set_tree_route(request, set_id):
    """
    TODO@ Render the tree of units that exists within a set.

    Contexts:
    - Search set, preview units in set
    - Pre diagnosis
    - Learner view progress in set
    - Set complete

    NEXT STATE
    GET View Set Tree
        -> GET Choose Set    ...when set is complete
        -> GET Choose Unit   ...when in learn mode
        -> GET Learn Card    ...when in diagnosis
            (Unit auto chosen)
    """

    current_user = get_current_user(request)
    context = current_user.get_learning_context() if current_user else {}

    # If we are just previewing, don't update anything
    if set_id != context.get('set', {}).get('entity_id'):
        return 200, {}

    # If the set is complete, lead the learner to choose another set.
    elif False:  # TODO@ how do I know the set is complete?
        next = {
            'method': 'GET',
            'path': '/api/users/{user_id}/sets'
                    .format(user_id=current_user['id']),
        }
        current_user.set_learning_context(next=next, unit=None, set=None)

    # When in diagnosis, choose the unit and card automagically.
    elif False:  # TODO@ when am I in diagnosis mode?
        next = {
            'method': 'GET',
            'path': '/api/cards/{card_id}/learn'
                    .format(card_id=None),  # TODO@ pick a card
        }
        current_user.set_learning_context(next=next, unit=None, card=None)
        # TODO@ choose a unit and a card

    # When in learn mode, lead me to choose a unit.
    else:
        next = {
            'method': 'GET',
            'path': '/api/sets/{set_id}/units'
                    .format(set_id=set_id),
        }
        current_user.set_learning_context(next=next)

    # TODO@ For the menu, it must return the name and ID of the set
    return 200, {
        'next': next,
    }


@get('/api/sets/{set_id}/units')
def get_set_units_route(request, set_id):
    """
    Present a small number of units the learner can choose from.

    NEXT STATE
    GET Choose Unit
        -> POST Choose Unit
    """

    current_user = get_current_user(request)
    if not current_user:
        return abort(401)

    context = current_user.get_learning_context()
    next = {
        'method': 'POST',
        'path': '/api/sets/{set_id}/units/{unit_id}'
                  .format(set_id=context.get('set', {}).get('entity_id'),
                          unit_id='{unit_id}'),
    }
    current_user.set_learning_context(next=next)

    set_ = Set.get_latest_accepted(set_id)

    # TODO@ Pull a list of 3 or 4 units to choose from
    #       based on priority
    # TODO Time estimates per unit for mastery
    units = []

    return 200, {
        'next': next,
        'units': [unit.deliver() for unit in units],
        # For the menu, it must return the name and ID of the set
        'set': set_.deliver(),
        'current_unit_id': context.get('unit', {}).get('entity_id'),
    }


@post('/api/sets/{set_id}/units/{unit_id}')
def choose_unit_route(request, set_id, unit_id):
    """
    Updates the learner's information based on the unit they have chosen.

    NEXT STATE
    POST Chosen Unit
        -> GET Learn Card
    """

    current_user = get_current_user(request)
    if not current_user:
        return abort(401)

    unit = Unit.get_latest_accepted(unit_id)
    if not unit:
        return abort(404)

    # If the unit isn't in the set...
    context = current_user.get_learning_context()
    set_ids = [set_['entity_id'] for set_ in Set.list_by_unit_id(unit_id)]
    if context.get('set', {}).get('entity_id') not in set_ids:
        return abort(400)

    # TODO@ Or, the unit doesn't need to be learned...
    if False:
        return abort(400)

    # TODO@ Choose a card for the learner to learn

    next = {
        'method': 'GET',
        'path': '/api/cards/{card_id}/learn'
                .format(card_id=None),  # TODO@
    }
    current_user.set_learning_context(unit=unit.data, next=next)

    return 200, {'next': next}
