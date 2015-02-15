from models.card import Card
from modules.validations import is_required, is_string, is_list, is_boolean
from modules.content import get as c


def is_list_of_options(options):
    """
    Ensure the list of options matches the expected format.
    """

    ok, has_correct = True, False

    for option in options:
        if not isinstance(option, dict):
            ok = False
        if 'value' not in option or not isinstance(option['value'], str):
            ok = False
        if 'correct' not in option or not isinstance(options['correct'], bool):
            ok = False
        if option.get('correct') is True:
            has_correct = True
        if 'feedback' not in option or not isinstance(option['feedback'], str):
            ok = False

    if not ok:
        return c('card', 'error_options')

    if not has_correct:
        return c('card', 'error_need_correct')


class MatchCard(Card):
    schema = dict(Card.schema.copy(), **{
        'body': {  # Question field
            'validate': (is_required, is_string,)
        },
        'options': {  # Available answers
            'validate': (is_required, is_list, is_list_of_options,),
        },
        'default_incorrect_feedback': {
            'validate': (is_required, is_string,)
        },
        'case_sensitive': {
            'validate': (is_boolean,),
            'default': False,
        }
    })

    def __init__(self, fields=None):
        """

        """
        super().__init__(self, fields)
        self['kind'] = 'match'
