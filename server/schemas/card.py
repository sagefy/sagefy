from schemas.entity_base import schema as entity_schema
from modules.validations import is_required, is_list, is_string, is_one_of
from modules.util import extend
import rethinkdb as r
from database.entity_base import list_by_entity_ids, find_requires_cycle

"""
Cards are the smallest entity in the Sagefy data structure system.
A card represents a single learner activity.
A card could present information, ask the learner to answer a question,
collaborate with a small group to tackle a challenge,
or create other cards.
"""

assessment_kinds = ('choice', 'number', 'match', 'formula',
                    'writing', 'upload', 'embed')

asynchronous_kinds = ('writing', 'upload', 'embed')


def is_valid_unit(schema, data, db_conn):
    query = (r.table('units')
              .filter(r.row['entity_id'] == data['unit_id'])
              .filter(r.row['status'].eq('accepted'))
              .limit(1))
    units = query.run(db_conn)
    if not units:
        return [{'name': 'unit_id', 'message': 'Not a valid unit.'}]
    return []


def ensure_requires(schema, data, db_conn):
    """

    """

    cards = list_by_entity_ids('cards', db_conn, data['require_ids'])
    if len(data['require_ids']) != len(cards):
        return [{'message': 'Didn\'t find all requires.'}]
    return []


def ensure_no_cycles(schema, data, db_conn):
    """
    Ensure no require cycles form.
    """

    if find_requires_cycle('cards', data, db_conn):
        return [{'message': 'Found a cycle in requires.'}]

    return []


schema = extend({}, entity_schema, {
    'tablename': 'cards',
    'fields': {
        'unit_id': {
            'validate': (is_required, is_string,)
        },
        'require_ids': {
            'validate': (is_list,),
            'default': []
        },
        'kind': {
            'validate': (is_required, is_string,
                         (is_one_of, 'video',  # 'page', 'audio', 'slideshow',
                                     'choice',  # 'number', 'match', 'formula',
                                     # 'writing', 'upload', 'embed'
                                     # only video & choice to start
                          ))
        },
    },
    'validate': (is_valid_unit, ensure_requires, ensure_no_cycles),
})
