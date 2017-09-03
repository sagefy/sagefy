from schemas.entity_base import schema as entity_schema
from modules.util import extend

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

schema = extend({}, entity_schema, {
    'tablename': 'cards',
    'fields': {
        'unit_id': {},
        'require_ids': {},
        'kind': {},
        'data': {},
    },
})
