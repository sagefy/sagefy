from schemas.entity_base import schema as entity_schema
from modules.util import extend
from database.entity_base import find_requires_cycle
from database.unit import list_latest_accepted_units

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


def ensure_requires(db_conn, schema, data):
    """

    """

    units = list_latest_accepted_units(db_conn, data['require_ids'])
    if len(data['require_ids']) != len(units):
        return [{'message': 'Didn\'t find all requires.'}]
    return []


def ensure_no_cycles(db_conn, schema, data):
    """
    Ensure no require cycles form.
    """

    if find_requires_cycle(db_conn, 'units', data):
        return [{'message': 'Found a cycle in requires.'}]
    return []


schema = extend({}, entity_schema, {
    'tablename': 'units',
    'fields': {
        'body': {},
        'require_ids': {},
    },
    'validate': (ensure_requires, ensure_no_cycles),
})
