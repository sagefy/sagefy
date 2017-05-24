from schemas.entity_base import schema as entity_schema
from modules.validations import is_required, is_string, is_list, \
    has_min_length
from modules.util import extend
from database.entity_base import list_by_entity_ids, find_requires_cycle

"""
A unit is the medium size in the Sagefy data structure system.
A unit represents a unit of learning activity.
A unit is defined by a single goal (objective). See Bloom’s Taxonomy.
A unit should represent a goal that is as small as possible
without becoming systemically redundant.
An example of a unit is a small learning lesson,
which may contain about five to eight minutes of information and
30-60 minutes of practice to gain proficiency.
"""


def ensure_requires(schema, data, db_conn):
    """

    """

    units = list_by_entity_ids('units', db_conn, data['require_ids'])
    if len(data['require_ids']) != len(units):
        return [{'message': 'Didn\'t find all requires.'}]
    return []


def ensure_no_cycles(schema, data, db_conn):
    """
    Ensure no require cycles form.
    """

    if find_requires_cycle('units', data, db_conn):
        return [{'message': 'Found a cycle in requires.'}]
    return []


schema = extend({}, entity_schema, {
    'tablename': 'units',
    'fields': {
        'body': {
            'validate': (is_required, is_string, (has_min_length, 1),)
        },
        'require_ids': {
            'validate': (is_list,),
            'default': []
        },
    },
    'validate': [ensure_requires, ensure_no_cycles],
})
