from random import shuffle
from schemas.card import schema as card_schema
from copy import deepcopy
from database.util import deliver_fields


# TODO all saves should go to ES


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

    schema = card_schema
    data = deepcopy(data)

    if access is 'learn':
        if data['order'] == 'random':
            shuffle(data['options'])

        if data['max_options_to_show']:
            data['options'] = data['options'][:data['max_options_to_show']]

    return deliver_fields(schema, data, access)
