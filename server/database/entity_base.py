from framework.elasticsearch import es
from modules.util import json_prep


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
