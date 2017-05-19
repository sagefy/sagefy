# MMM
from schemas.entity_base import schema as entity_schema
from modules.util import extend
from modules.validations import is_required, is_string, is_list, is_one_of, \
    has_min_length
import rethinkdb as r

"""
A subject is a collection of units and other subjects.
Subjects can vary greatly in scale.
A graph is automatically formed based on the units and subjects specified.
"""


def is_valid_members(schema, data, db_conn):
    """

    """

    # TODO-3 this is going to be slow
    for member_desc in data['members']:
        query = (r.table(member_desc['kind'] + 's')
                  .filter(r.row['status'].eq('accepted'))
                  .filter(r.row['entity_id'] == member_desc['id']))
        vs = [e for e in query.run(db_conn)]
        if not vs:
            return [{
                'message': 'Not a valid entity.',
                'value': member_desc['id'],
            }]

    return []


def ensure_no_cycles(schema, data, db_conn):
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
        entities = Subject.list_by_entity_ids(db_conn, entity_ids)
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
        'body': {
            'validate': (is_required, is_string, (has_min_length, 1),)
        },
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
    'validate': [is_valid_members, ensure_no_cycles],
})
