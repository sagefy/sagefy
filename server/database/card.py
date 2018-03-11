from random import shuffle
from copy import deepcopy
import uuid

from schemas.card import schema as card_schema
from schemas.cards.video_card import schema as video_card_schema
from schemas.cards.page_card import schema as page_card_schema
from schemas.cards.choice_card import schema as choice_card_schema
from schemas.cards.unscored_embed_card \
  import schema as unscored_embed_card_schema
from database.util import deliver_fields
from database.entity_base import save_entity_to_es
from database.util import insert_row, save_row, get_row, list_rows
from modules.util import convert_slug_to_uuid



def get_card_schema(data):
  if 'kind' in data:
    if data['kind'] == 'video':
      return video_card_schema
    if data['kind'] == 'page':
      return page_card_schema
    if data['kind'] == 'unscored_embed':
      return unscored_embed_card_schema
    if data['kind'] == 'choice':
      return choice_card_schema


def ensure_requires(db_conn, data):
  """

  """

  cards = list_latest_accepted_cards(db_conn, data.get('require_ids', []))
  if len(data.get('require_ids', [])) != len(cards):
    return [{
      'name': 'require_ids',
      'message': 'Didn\'t find all requires.',
      'ref': 'qbASvY61QNyI_MkYSgEhTQ',
    }]
  return []


def ensure_no_cycles(db_conn, data):
  """
  Ensure no require cycles form.
  """

  from database.entity_facade import find_requires_cycle

  if find_requires_cycle(db_conn, 'cards', data):
    return [{
      'name': 'require_ids',
      'message': 'Found a cycle in requires.',
      'ref': 'Vxd7Ed32S4WW1pumEIPRxg',
    }]
  return []


def insert_card(db_conn, data):
  """
  Create a new version of a new card, saving to ES.
  """

  schema = get_card_schema(data)
  if not schema:
    return None, [{
      'name': 'kind',
      'message': 'Missing card kind.',
      'ref': 'aQ58K_s6TAimzMegrIAk3g',
    }]
  query = """
    INSERT INTO cards_entity_id (entity_id)
    VALUES (%(entity_id)s);
    INSERT INTO cards
    (  entity_id  ,   name  ,   user_id  ,   unit_id  ,
       require_ids  ,   kind  ,   data  )
    VALUES
    (%(entity_id)s, %(name)s, %(user_id)s, %(unit_id)s,
     %(require_ids)s, %(kind)s, %(data)s)
    RETURNING *;
  """
  data = {
    'entity_id': uuid.uuid4(),
    'name': data['name'],
    'user_id': convert_slug_to_uuid(data['user_id']),
    'unit_id': convert_slug_to_uuid(data['unit_id']),
    'require_ids': [convert_slug_to_uuid(require_id)
                    for require_id in data.get('require_ids', [])],
    'kind': data.get('kind'),
    'data': data.get('data'),
  }
  errors = ensure_requires(db_conn, data) + ensure_no_cycles(db_conn, data)
  if errors:
    return None, errors
  data, errors = insert_row(db_conn, schema, query, data)
  if not errors:
    save_entity_to_es('card', deliver_card(data, access='view'))
  return data, errors


def insert_card_version(db_conn, current_data, next_data):
  """
  Create a new version of an existing card, saving to ES.
  """

  schema = get_card_schema(current_data)
  if not schema:
    return None, [{
      'name': 'kind',
      'message': 'Missing card kind.',
      'ref': 'xASOK-O6Qw-8f2shCrHs9A',
    }]
  query = """
    INSERT INTO cards
    (  entity_id  ,   previous_id  ,   name  ,   user_id  ,   unit_id  ,
       require_ids  ,   kind  ,   data  )
    VALUES
    (%(entity_id)s, %(previous_id)s, %(name)s, %(user_id)s, %(unit_id)s,
     %(require_ids)s, %(kind)s, %(data)s)
    RETURNING *;
  """
  data = {
    'entity_id': current_data['entity_id'],
    'previous_id': current_data['version_id'],
    'user_id': convert_slug_to_uuid(next_data['user_id']),
    'kind': current_data['kind'],
    'name': next_data.get('name') or current_data.get('name'),
    'unit_id': convert_slug_to_uuid(next_data.get('unit_id') or
                                    current_data.get('unit_id')),
    'require_ids': [convert_slug_to_uuid(require_id)
                    for require_id in next_data.get('require_ids')
                    or current_data.get('require_ids') or []],
    'data': next_data.get('data') or current_data.get('data'),
  }
  errors = ensure_requires(db_conn, data) + ensure_no_cycles(db_conn, data)
  if errors:
    return None, errors
  data, errors = insert_row(db_conn, schema, query, data)
  if not errors:
    save_entity_to_es('card', deliver_card(data, access='view'))
  return data, errors


def update_card(db_conn, version_id, status):
  """
  Update a card version's status and available. [hidden]
  """

  query = """
    UPDATE cards
    SET status = %(status)s
    WHERE version_id = %(version_id)s
    RETURNING *;
  """
  data = {
    'version_id': convert_slug_to_uuid(version_id),
    'status': status,
  }
  data, errors = save_row(db_conn, query, data)
  if not errors:
    save_entity_to_es('card', deliver_card(data, access='view'))
  return data, errors


def validate_card_response(card, response):
  """
  Ensure the given response body is valid,
  given the card information.
  """

  # If not a choice card, return [{'message': 'No response is valid.'}]

  ids = [opt['id'] for opt in card['data']['options']]
  if response not in ids:
    return [{
      'message': 'Value is not an option.',
      'ref': 'SOxwW64dTyCWdTAdp0ImdQ',
    }]
  return []


def score_card_response(card, response):
  """
  Score the given response.
  Returns the score and feedback.
  """

  # If not a choice card, raise Exception("No method implemented.")
  for opt in card['data']['options']:
    if response == opt['id']:
      if opt['correct']:
        return 1.0, opt['feedback']
      return 0.0, opt['feedback']
  return 0.0, 'Default error Vqjk9WHrR0CSVKQeZZ8svQ'


def deliver_card(data, access=None):
  """
  Overwrite to randomize option order and limit number of options.
  """

  schema = get_card_schema(data)
  if not schema:
    schema = card_schema
  data = deepcopy(data)
  kind = data['kind']
  order = data['data'].get('order')
  max_options_to_show = data['data'].get('max_options_to_show')
  if access == 'learn' and kind == 'choice':
    if order == 'random':
      shuffle(data['data']['options'])
    if max_options_to_show:
      data['data']['options'] = (data['data']['options']
                                 [:max_options_to_show])
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
  params = {'entity_ids': tuple([
    convert_slug_to_uuid(entity_id)
    for entity_id in entity_ids
  ])}
  return list_rows(db_conn, query, params)


def list_many_card_versions(db_conn, version_ids):
  """
  List Card Versions by VIDs
  """

  if not version_ids:
    return []
  query = """
    SELECT *
    FROM cards
    WHERE version_id in %(version_ids)s
    ORDER BY created DESC;
    /* TODO LIMIT OFFSET */
  """
  params = {'version_ids': tuple(
    convert_slug_to_uuid(vid)
    for vid in version_ids
  )}
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
  params = {'version_id': convert_slug_to_uuid(version_id)}
  return get_row(db_conn, query, params)


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
    WHERE %(entity_id)s = ANY(require_ids)
    ORDER BY created DESC;
    /* TODO LIMIT OFFSET */
  """
  params = {
    'entity_id': convert_slug_to_uuid(entity_id),
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
    'unit_id': convert_slug_to_uuid(unit_id),
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
