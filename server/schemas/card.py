from schemas.entity_base import schema as entity_schema
from modules.util import extend
from database.card import list_latest_accepted_cards
from database.entity_base import find_requires_cycle

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


def ensure_requires(db_conn, schema, data):
    """

    """

    cards = list_latest_accepted_cards(db_conn, data['require_ids'])
    if len(data['require_ids']) != len(cards):
        return [{'message': 'Didn\'t find all requires.'}]
    return []


def ensure_no_cycles(db_conn, schema, data):
    """
    Ensure no require cycles form.
    """

    if find_requires_cycle(db_conn, 'cards', data):
        return [{'message': 'Found a cycle in requires.'}]

    return []


schema = extend({}, entity_schema, {
    'tablename': 'cards',
    'fields': {
        'unit_id': {},
        'require_ids': {},
        'kind': {},
    },
    'validate': (ensure_requires, ensure_no_cycles),
})
