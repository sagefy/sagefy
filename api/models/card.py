from modules.model import Model
from modules.validations import is_required, is_language, is_boolean, \
    is_list, is_string, is_one_of
from modules.util import uniqid


class Card(Model):
    """
    Cards are the smallest entity in the Sagefy data structure system.
    A card represents a single learner activity.
    A card could present information, ask the learner to answer a question,
    collaborate with a small group to tackle a challenge,
    or create other cards.
    """
    tablename = 'cards'

    """
    The model represents a **version** of a card, not a card itself.
    The `entity_id` attribute is what refers to a particular card.
    The `id` attribute refers to a specific version of the card.
    The `previous_id` attribute refers to the version based off.
    """

    schema = dict(Model.schema.copy(), **{
        'entity_id': {
            'validate': (is_required, is_string,),
            'default': uniqid
        },
        'previous_id': {
            'validate': (is_string,),
        },
        'language': {
            'validate': (is_required, is_language,),
            'default': 'en'
        },
        'unit_id': {
            'validate': (is_required, is_string,)
        },
        'name': {
            'validate': (is_required, is_string,)
        },
        'canonical': {
            'validate': (is_boolean,),
            'default': False
        },
        'tags': {
            'validate': (is_list,),
            'default': []
        },
        'requires_ids': {
            'validate': (is_list,),
            'default': []
        },
        'kind': {
            'validate': (is_required, is_string,
                         (is_one_of, 'video', 'choice'))
        }
    })

    # TODO: Ensure no require cycles form
