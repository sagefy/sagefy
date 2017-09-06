from random import shuffle
from schemas.card import schema as card_schema
from schemas.cards.video_card import schema as video_card_schema
from schemas.cards.choice_card import schema as choice_card_schema
from copy import deepcopy
from database.util import deliver_fields
from database.entity_base import save_entity_to_es
from database.util import insert_row, update_row, get_row, list_rows
from modules.util import convert_slug_to_uuid


def get_card_schema(data):
    if 'kind' in data:
        if data['kind'] == 'video':
            return video_card_schema
        if data['kind'] == 'choice':
            return choice_card_schema


def ensure_requires(db_conn, data):
    """

    """

    cards = list_latest_accepted_cards(db_conn, data['require_ids'])
    if len(data['require_ids']) != len(cards):
        return [{'message': 'Didn\'t find all requires.'}]
    return []


def ensure_no_cycles(db_conn, data):
    """
    Ensure no require cycles form.
    """

    from database.entity_facade import find_requires_cycle

    if find_requires_cycle(db_conn, 'cards', data):
        return [{'message': 'Found a cycle in requires.'}]
    return []


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
    query = """
        WITH temp AS (
            INSERT INTO cards_entity_id (entity_id)
            VALUES (uuid_generate_v4())
            RETURNING entity_id
        )
        INSERT INTO cards
        (entity_id  ,   name  ,   user_id  ,   unit_id  ,
           require_ids  ,   kind  ,   data  )
        SELECT
         entity_id  , %(name)s, %(user_id)s, %(unit_id)s,
         %(require_ids)s, %(kind)s, %(data)s
        FROM temp
        RETURNING *;
    """
    errors = ensure_requires(db_conn, data) + ensure_no_cycles(db_conn, data)
    if errors:
        return None, errors
    data, errors = insert_row(db_conn, schema, query, data)
    if not errors:
        save_entity_to_es('card', deliver_card(data, access='view'))
    return data, errors


# TODO insert card version, adding in previous version
"""
    previous_id = None  # TODO-1
    latest = get_latest_accepted_card(db_conn, entity_id)
    # if latest: data['previous_id'] = latest['version_id']
    data = {
        FALSE
    }
"""


def update_card(db_conn, prev_data, data):
    """
    Update a card version's status and available. [hidden]
    """

    schema = get_card_schema(data)
    if not schema:
        return data, [{
            'name': 'kind',
            'message': 'Missing card kind.',
        }]
    query = """
        UPDATE cards
        SET status = %(status)s
        WHERE version_id = %(version_id)s
        RETURNING *;
    """
    data = {
        'id': convert_slug_to_uuid(prev_data['id']),
    }
    data, errors = update_row(db_conn, schema, query, prev_data, data)
    if not errors:
        save_entity_to_es('card', deliver_card(data, access='view'))
    return data, errors


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


def get_latest_accepted_card(db_conn, entity_id):
    """
    Get Latest Accepted Card Version by EID
    """

    query = """
        SELECT DISTINCT ON (entity_id) *
        FROM cards
        WHERE status = 'accepted' AND entity_id = %(entity_id)s
        ORDER BY entity_id, created DESC;
        /* TODO LIMIT */
    """
    params = {
        'entity_id': convert_slug_to_uuid(entity_id),
    }
    return get_row(db_conn, query, params)


def list_latest_accepted_cards(db_conn, entity_ids):
    """
    List Latest Accepted Card Versions by EIDs
    """

    if not entity_ids:
        return []
    query = """
        SELECT DISTINCT ON (entity_id) *
        FROM cards
        WHERE status = 'accepted' AND entity_id in %(entity_ids)s
        ORDER BY entity_id, created DESC;
        /* TODO LIMIT OFFSET */
    """
    params = {'entity_ids': tuple(entity_ids)}
    return list_rows(db_conn, query, params)


def list_many_card_versions(db_conn, version_ids):
    """
    List Card Versions by VIDs
    """

    query = """
        SELECT *
        FROM cards
        WHERE version_id in %(version_ids)s
        ORDER BY created DESC;
        /* TODO LIMIT OFFSET */
    """
    params = {'version_ids': version_ids}
    return list_rows(db_conn, query, params)


def get_card_version(db_conn, version_id):
    """
    Get a card version.
    """

    query = """
        SELECT *
        FROM cards
        WHERE version_id = %(version_id)s
        ORDER BY created DESC;
        /* TODO LIMIT OFFSET */
    """
    params = {'version_id': version_id}
    return list_rows(db_conn, query, params)


def list_one_card_versions(db_conn, entity_id):
    """
    List Card Versions by EID
    """

    query = """
        SELECT *
        FROM cards
        WHERE entity_id = %(entity_id)s
        ORDER BY created DESC;
        /* TODO LIMIT OFFSET */
    """
    params = {'entity_id': convert_slug_to_uuid(entity_id)}
    return list_rows(db_conn, query, params)


def list_required_cards(db_conn, entity_id):
    """
    List Latest Version of Required Cards by EID
    """

    later_card = get_latest_accepted_card(db_conn, entity_id)
    return list_latest_accepted_cards(db_conn, later_card['require_ids'])


def list_required_by_cards(db_conn, entity_id):
    """
    List Latest Version of Required By Cards by EID
    """

    query = """
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
    params = {
        'entity_id': entity_id,
    }
    return list_rows(db_conn, query, params)


def list_random_cards_in_unit(db_conn, unit_id, limit=10):
    """
    Choose 10 random cards from the DB within a given unit.
    """

    query = """
        WITH temp as (
            SELECT DISTINCT ON (entity_id) *
            FROM cards
            WHERE status = 'accepted'
            ORDER BY entity_id, created DESC
        )
        SELECT *
        FROM temp
        WHERE unit_id = %(unit_id)s
        ORDER BY random()
        LIMIT %(limit)s;
    """
    params = {
        'limit': limit,
        'unit_id': unit_id,
    }
    return list_rows(db_conn, query, params)


def list_all_card_entity_ids(db_conn):
    """
    List all card entity ids.
    """

    query = """
        SELECT entity_id
        FROM cards;
    """
    params = {}
    return [
        row['entity_id']
        for row in list_rows(db_conn, query, params)
    ]
