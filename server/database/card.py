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

    *M2P Insert Card Version

        WITH temp AS (
            INSERT INTO cards_entity_id (entity_id) VALUES (uuid_generate_v4())
            RETURNING entity_id
        )
        INSERT INTO cards
        (entity_id  ,   previous_id  ,   name  ,   user_id  ,   unit_id  ,
           require_ids  ,   kind  ,   data  )
        SELECT
         entity_id  , %(previous_id)s, %(name)s, %(user_id)s, %(unit_id)s,
         %(require_ids)s, %(kind)s, %(data)s
        FROM temp
        RETURNING *;
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

    *M2P Update Card Version Status [hidden]

        UPDATE cards
        SET status = %(status)s
        WHERE version_id = %(version_id)s
        RETURNING *;
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

    if access is 'learn' and data['kind'] is 'choice':
        if data['order'] == 'random':
            shuffle(data['options'])

        if data['max_options_to_show']:
            data['options'] = data['options'][:data['max_options_to_show']]

    return deliver_fields(schema, data, access)


"""
*M2P Get Latest Accepted Card Version by EID

    SELECT DISTINCT ON (entity_id) *
    FROM cards
    WHERE status = 'accepted' AND entity_id = %(entity_id)s
    ORDER BY entity_id, created DESC;
    /* TODO LIMIT */

*M2P List Latest Accepted Card Versions by EIDs

    SELECT DISTINCT ON (entity_id) *
    FROM cards
    WHERE status = 'accepted' AND entity_id in %(entity_ids)s
    ORDER BY entity_id, created DESC;
    /* TODO LIMIT OFFSET */

*M2P List Card Versions by VIDs

    SELECT *
    FROM cards
    WHERE version_id in %(version_ids)s
    ORDER BY created DESC;
    /* TODO LIMIT OFFSET */

*M2P List Card Versions by EID

    SELECT *
    FROM cards
    WHERE entity_id = %(entity_id)s
    ORDER BY created DESC;
    /* TODO LIMIT OFFSET */

*M2P List Latest Version of Required Cards by EID

    1. Get Latest Accepted Card Version by EID
    2. List Latest Accepted Card Versions by EIDs (require_ids)

*M2P List Latest Version of Required By Cards by EID

    WITH temp as (
        SELECT DISTINCT ON (entity_id) *
        FROM cards
        WHERE status = 'accepted'
        ORDER BY entity_id, created DESC
    )
    SELECT *
    FROM temp
    WHERE %(entity_id)s in require_ids
    ORDER BY created DESC;
    /* TODO LIMIT OFFSET */
"""
