from random import shuffle
from schemas.card import schema as card_schema
from schemas.cards.video_card import schema as video_card_schema
from schemas.cards.choice_card import schema as choice_card_schema
from copy import deepcopy
from database.util import deliver_fields
from database.entity_base import insert_entity, update_entity, \
    save_entity_to_es


def get_card_schema(data):
    if 'kind' in data:
        if data['kind'] == 'video':
            return video_card_schema
        if data['kind'] == 'choice':
            return choice_card_schema


def insert_card(db_conn, data):
    """
    Create a card, saving to ES.
    """

    schema = get_card_schema(data)
    if not schema:
        return data, [{
            'name': 'kind',
            'message': 'Missing card kind.',
        }]
    card, errors = insert_entity(schema, db_conn, data)
    if not errors:
        save_entity_to_es('card', deliver_card(card, access='view'))
    return card, errors


def update_card(prev_data, data, db_conn):
    """
    Update a card.
    """

    schema = get_card_schema(data)
    if not schema:
        return data, [{
            'name': 'kind',
            'message': 'Missing card kind.',
        }]
    card, errors = update_entity(schema, prev_data, data, db_conn)
    if not errors:
        save_entity_to_es('card', deliver_card(card, access='view'))
    return card, errors


def validate_card_response(card, response):
    """
    Ensure the given response body is valid,
    given the card information.
    """

    # If not a choice card, return [{'message': 'No response is valid.'}]

    values = [opt['value'] for opt in card['options']]
    if response not in values:
        return [{'message': 'Value is not an option.'}]
    return []


def score_card_response(card, response):
    """
    Score the given response.
    Returns the score and feedback.
    """

    # If not a choice card, raise Exception("No method implemented.")

    for opt in card['options']:
        if response == opt['value']:
            if opt['correct']:
                return 1.0, opt['feedback']
            else:
                return 0.0, opt['feedback']

    return 0.0, 'Default error ajflsdvco'


def deliver_card(data, access=None):
    """
    Overwrite to randomize option order and limit number of options.
    """

    schema = get_card_schema(data)
    if not schema:
        schema = card_schema
    data = deepcopy(data)

    if access is 'learn':
        if data['order'] == 'random':
            shuffle(data['options'])

        if data['max_options_to_show']:
            data['options'] = data['options'][:data['max_options_to_show']]

    return deliver_fields(schema, data, access)
