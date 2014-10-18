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
        return Card.get_latest(entity_id)
    elif kind is 'unit':
        return Unit.get_latest(entity_id)
    elif kind is 'set':
        return Set.get_latest(entity_id)


def get_kind(json):
    """
    Given the JSON data, figure out what kind of entity lies within.
    """
    if json.get('card'):
        return 'card'
    elif json.get('unit'):
        return 'unit'
    elif json.get('set'):
        return 'set'


def create_entity(json):
    """
    Given a kind and some json, call insert on that kind
    and return the results.
    """
    if json.get('card'):
        return Card.insert(json.card)
    elif json.get('unit'):
        return Unit.insert(json.unit)
    elif json.get('set'):
        return Set.insert(json.set)
