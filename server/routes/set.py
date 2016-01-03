from framework.routes import get, post, abort
from models.set import Set
from models.topic import Topic
from models.unit import Unit
from framework.session import get_current_user
from modules.sequencer.traversal import traverse, judge
from modules.sequencer.card_chooser import choose_card

# Nota Bene: We use `set_` because `set` is a type in Python


@get('/s/sets/{set_id}')
def get_set_route(request, set_id):
    """
    Get a specific set given an ID.
    """

    set_ = Set.get_latest_accepted(set_id)
    if not set_:
        return abort(404)

    # TODO-2 SPLITUP create new endpoints for these instead
    topics = Topic.list_by_entity_id(entity_id=set_id)
    versions = Set.get_versions(entity_id=set_id)
    units = set_.list_units()

    return 200, {
        'set': set_.deliver(),
        # 'set_parameters': set_.fetch_parameters(),
        'topics': [topic.deliver() for topic in topics],
        'versions': [version.deliver() for version in versions],
        'units': [unit.deliver() for unit in units],
    }


@get('/s/sets/{set_id}/versions')
def get_set_versions_route(request, set_id):
    """
    Get versions set given an ID. Paginates.
    """

    versions = Set.get_versions(entity_id=set_id, **request['params'])
    return 200, {
        'versions': [version.deliver(access='view') for version in versions]
    }


@get('/s/sets/{set_id}/tree')
def get_set_tree_route(request, set_id):
    """
    Render the tree of units that exists within a set.

    Contexts:
    - Search set, preview units in set
    - Pre diagnosis
    - Learner view progress in set
    - Set complete

    NEXT STATE
    GET View Set Tree
        -> GET Choose Set    ...when set is complete
        -> GET Choose Unit   ...when in learn or review mode
        -> GET Learn Card    ...when in diagnosis
            (Unit auto chosen)

    TODO-2 merge with get_set_units_route
    TODO-2 simplify this method
    """

    set_ = Set.get(entity_id=set_id)

    if not set_:
        return abort(404)

    units = set_.list_units()

    # For the menu, it must return the name and ID of the set
    output = {
        'set': set_.deliver(),
        'units': [u.deliver() for u in units],
    }

    current_user = get_current_user(request)

    if not current_user:
        return 200, output

    context = current_user.get_learning_context() if current_user else {}
    buckets = traverse(current_user, set_)
    output['buckets'] = {
        'diagnose': [u['entity_id'] for u in buckets['diagnose']],
        'review': [u['entity_id'] for u in buckets['review']],
        'learn': [u['entity_id'] for u in buckets['learn']],
        'done': [u['entity_id'] for u in buckets['done']],
    }

    # If we are just previewing, don't update anything
    if set_id != context.get('set', {}).get('entity_id'):
        return 200, output

    # When in diagnosis, choose the unit and card automagically.
    if buckets['diagnose']:
        unit = buckets['diagnose'][0]
        card = choose_card(current_user, unit)
        next_ = {
            'method': 'GET',
            'path': '/s/cards/{card_id}/learn'
                    .format(card_id=card['entity_id']),
        }
        current_user.set_learning_context(
            next=next_, unit=unit.data, card=card.data)

    # When in learn or review mode, lead me to choose a unit.
    elif buckets['review'] or buckets['learn']:
        next_ = {
            'method': 'GET',
            'path': '/s/sets/{set_id}/units'
                    .format(set_id=set_id),
        }
        current_user.set_learning_context(next=next_)

    # If the set is complete, lead the learner to choose another set.
    else:
        next_ = {
            'method': 'GET',
            'path': '/s/users/{user_id}/sets'
                    .format(user_id=current_user['id']),
        }
        current_user.set_learning_context(next=next_, unit=None, set=None)

    output['next'] = next_
    return 200, output


@get('/s/sets/{set_id}/units')
def get_set_units_route(request, set_id):
    """
    Present a small number of units the learner can choose from.

    NEXT STATE
    GET Choose Unit
        -> POST Choose Unit
    """

    # TODO-3 simplify this method. should it be part of the models?

    current_user = get_current_user(request)
    if not current_user:
        return abort(401)

    context = current_user.get_learning_context()
    next_ = {
        'method': 'POST',
        'path': '/s/sets/{set_id}/units/{unit_id}'
                  .format(set_id=context.get('set', {}).get('entity_id'),
                          unit_id='{unit_id}'),
    }
    current_user.set_learning_context(next=next_)

    set_ = Set.get_latest_accepted(set_id)

    # Pull a list of up to 5 units to choose from based on priority.
    buckets = traverse(current_user, set_)
    units = buckets['learn'][:5]
    # TODO-3 Time estimates per unit for mastery.

    return 200, {
        'next': next_,
        'units': [unit.deliver() for unit in units],
        # For the menu, it must return the name and ID of the set
        'set': set_.deliver(),
        'current_unit_id': context.get('unit', {}).get('entity_id'),
    }


@post('/s/sets/{set_id}/units/{unit_id}')
def choose_unit_route(request, set_id, unit_id):
    """
    Updates the learner's information based on the unit they have chosen.

    NEXT STATE
    POST Chosen Unit
        -> GET Learn Card
    """

    # TODO-3 simplify this method. should it be broken up or moved to model?

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

    status = judge(unit, current_user)
    # Or, the unit doesn't need to be learned...
    if status == "done":
        return abort(400)

    # Choose a card for the learner to learn
    card = choose_card(current_user, unit)

    if card:
        next_ = {
            'method': 'GET',
            'path': '/s/cards/{card_id}/learn'
                    .format(card_id=card['entity_id']),
        }
    else:
        next_ = {}

    current_user.set_learning_context(
        unit=unit.data,
        card=card.data if card else None,
        next=next_
    )

    return 200, {'next': next_}
