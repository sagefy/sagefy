"""
Facades for working with entities (card, unit, set).
"""

from models.card import Card
from models.unit import Unit
from models.set import Set


def get_latest_canonical(kind, entity_id):
    """
    Given a kind and an entity_id, pull the latest canonical
    version out of the database.
    """

    if kind is 'card':
        return Card.get_latest_canonical(entity_id)
    elif kind is 'unit':
        return Unit.get_latest_canonical(entity_id)
    elif kind is 'set':
        return Set.get_latest_canonical(entity_id)


def get_kind(data):
    """
    Given the JSON data, figure out what kind of entity lies within.
    """

    kinds = []

    if 'card' in data or 'cards' in data:
        kinds.append('card')
    elif 'unit' in data or 'units' in data:
        kinds.append('unit')
    elif 'set' in data or 'set' in data:
        kinds.append('set')

    if len(kinds) == 0:
        return None
    if len(kinds) == 1:
        return kinds[0]

    return kinds


def create_entity(data):
    """
    Given a kind and some json, call insert on that kind
    and return the results.
    """

    if 'card' in data:
        return Card.insert(data['card'])
    elif 'unit' in data:
        return Unit.insert(data['unit'])
    elif 'set' in data:
        return Set.insert(data['set'])

    return None, []
