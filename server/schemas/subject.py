from schemas.entity_base import schema as entity_schema
from modules.util import extend
from modules.validations import is_required, is_string, is_list, is_one_of

"""
A subject is a collection of units and other subjects.
Subjects can vary greatly in scale.
A graph is automatically formed based on the units and subjects specified.
"""


def is_valid_members(db_conn, schema, data):
    """

    """

    # TODO-3 this is going to be slow
    for member_desc in data['members']:
        entity_id, kind = member_desc['id'], member_desc['kind']
        entity = None
        if kind == 'unit':
            entity = get_latest_accepted_unit(entity_id)
        elif kind == 'subject':
            entity = get_latest_accepted_subject(entity_id)
        if not entity:
            return [{
                'message': 'Not a valid entity.',
                'value': entity_id,
            }]

    return []


def ensure_no_cycles(db_conn, schema, data):
    """
    Ensure no membership cycles form.
    """

    seen = set()
    main_id = data['entity_id']
    found = {'cycle': False}

    def _(members):
        if found['cycle']:
            return
        entity_ids = [
            member['id']
            for member in members
            if member['kind'] == 'subject'
        ]
        entities = list_latest_accepted_subjects(db_conn, entity_ids)
        for entity in entities:
            if entity['entity_id'] == main_id:
                found['cycle'] = True
                break
            if entity['entity_id'] not in seen:
                seen.add(entity['entity_id'])
                _(entity['members'])

    _(data['members'])

    if found['cycle']:
        return [{'message': 'Found a cycle in membership.'}]

    return []


schema = extend({}, entity_schema, {
    'tablename': 'subjects',
    'fields': {
        'body': {},
        'members': {
            'validate': (is_required, is_list,),
            'embed_many': {
                'id': {
                    'validate': (is_required, is_string,),
                },
                'kind': {
                    'validate': (is_required, is_string, (
                        is_one_of, 'unit', 'subject'
                    )),
                }
            }
        }
    },
    'validate': (is_valid_members, ensure_no_cycles),
})
