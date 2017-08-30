from framework.elasticsearch import es
from modules.util import json_prep
from modules.util import omit, pick
from database.util import insert_document, update_document


def start_accepted_query(tablename):
    """
    Begins the query by reducing the table down
    to the latest accepted versions for each.
    """

    assert tablename in ('cards', 'units', 'subjects')
    # TODO-2 this query should have an index in card, unit, subject
    # TODO-2 is there a way to avoid the cost of this query?
    return (r.table(tablename)
             .filter(r.row['status'].eq('accepted'))
             .group('entity_id')
             .max('created')
             .default(None)
             .ungroup()
             .map(r.row['reduction']))


def get_latest_accepted(db_conn, tablename, entity_id):
    """
    Get the latest accepted version of the card.
    """

    assert tablename in ('cards', 'units', 'subjects')

    if not entity_id:
        return

    # TODO-2 this query should have an index in card, unit, subject
    query = (start_accepted_query(tablename)
             .filter(r.row['entity_id'] == entity_id)
             .limit(1))

    documents = list(query.run(db_conn))

    if len(documents) > 0:
        return documents[0]


def list_by_entity_ids(db_conn, tablename, entity_ids):
    """
    Get a list of entities by a list of entity IDs.
    """

    assert tablename in ('cards', 'units', 'subjects')
    if not entity_ids:
        return []

    query = (start_accepted_query(tablename)
             .filter(lambda entity:
                     r.expr(entity_ids)
                     .contains(entity['entity_id'])))

    docs = query.run(db_conn)
    return [fields for fields in docs]
    # TODO-2 index in unit and subject


def list_by_version_ids(db_conn, tablename, version_ids):
    """
    ???
    """

    assert tablename in ('cards', 'units', 'subjects')
    if not version_ids:
        return []

    query = (r.table(tablename)
              .filter(lambda entity:
                      r.expr(version_ids)
                      .contains(entity['id']))
              .filter(r.row['status'].eq('accepted')))
    docs = query.run(db_conn)
    entity_ids = [fields['entity_id'] for fields in docs]
    return list_by_entity_ids(db_conn, tablename, entity_ids)


def get_versions(db_conn, tablename, entity_id, limit=10, skip=0, **params):
    """
    Get the latest accepted version of the card.
    """

    assert tablename in ('cards', 'units', 'subjects')
    if not entity_id:
        return []

    # TODO-2 this query should have an index in card, unit, subject
    query = (r.table(tablename)
              .filter(r.row['entity_id'] == entity_id)
              .order_by(r.desc('created'))
              .skip(skip)
              .limit(limit))

    return [fields for fields in query.run(db_conn)]


def list_requires(db_conn, tablename, entity_id, limit=10, skip=0, **params):
    """
    Get the same kind of entity that this one requires.
    """

    assert tablename in ('cards', 'units', 'subjects')
    if not entity_id:
        return []

    entity = get_latest_accepted(db_conn, tablename, entity_id=entity_id)

    # TODO-2 this query should have an index in card and unit
    query = (start_accepted_query(tablename)
             .filter(lambda _: r.expr(entity['require_ids'])
                                .contains(_['entity_id']))
             .order_by(r.desc('created'))
             .skip(skip)
             .limit(limit))

    return [fields for fields in query.run(db_conn)]


def list_required_by(tablename, db_conn, entity_id,
                     limit=10, skip=0, **params):
    """
    Get the same kind of entity that requires this one.
    """

    assert tablename in ('cards', 'units', 'subjects')
    if not entity_id:
        return []

    # TODO-2 this query should have an index in card and unit
    query = (start_accepted_query(tablename)
             .filter(r.row['require_ids'].contains(entity_id))
             .order_by(r.desc('created'))
             .skip(skip)
             .limit(limit))

    return [fields for fields in query.run(db_conn)]


def insert_entity(db_conn, schema, data):
    """
    When a user creates a new version,
    don't accept certain fields.

    Also, find the previous_id.
    """

    data = omit(data, ('version_id', 'status', 'available', 'previous_id'))
    if 'entity_id' in data:
        latest = get_latest_accepted(
            schema['tablename'], db_conn, data['entity_id'])
        if latest:
            data['previous_id'] = latest['id']
    return insert_document(db_conn, schema, data)


def update_entity(db_conn, schema, prev_data, data):
    """
    Only allow changes to the status on update.
    """

    data = pick(data, ('status', 'available'))
    return update_document(db_conn, schema, prev_data, data)


def save_entity_to_es(kind, data):
    """
    Overwrite save method to add to Elasticsearch.
    """

    # NB use deliver_thing(entity) BEFORE calling this function
    body = json_prep(data)
    if data['status'] == 'accepted':
        return es.index(
            index='entity',
            doc_type=kind,
            body=body,
            id=data['entity_id'],
        )


def find_requires_cycle(db_conn, tablename, data):
    """
    Inspect own requires to see if a cycle is formed.
    """

    assert tablename in ('cards', 'units', 'subjects')

    seen = set()
    main_id = data['entity_id']
    found = {'cycle': False}

    def _(require_ids):
        if found['cycle']:
            return
        entities = list_by_entity_ids(db_conn, tablename, require_ids)
        for entity in entities:
            if entity['entity_id'] == main_id:
                found['cycle'] = True
                break
            if entity['entity_id'] not in seen:
                seen.add(entity['entity_id'])
                if 'require_ids' in entity:
                    _(entity['require_ids'])

    _(data['require_ids'])

    return found['cycle']


def get_version(db_conn, tablename, version_id):
    """
    Retrieve a specific version from the database.
    """

    assert tablename in ('cards', 'units', 'subjects')
    return r.table(tablename).get(version_id).run(db_conn)
