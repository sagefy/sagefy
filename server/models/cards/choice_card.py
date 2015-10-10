from models.card import Card
from modules.validations import is_required, is_string, is_list, \
    is_one_of, is_boolean, is_integer, has_min_length
from modules.content import get as c


def has_correct_options(options):
    """
    Ensure the list of options has at least one correct option.
    """

    has_correct = False

    for option in options:
        if option.get('correct') is True:
            has_correct = True

    if not has_correct:
        return c('error_need_correct')


class ChoiceCard(Card):
    schema = dict(Card.schema.copy(), **{
        'body': {  # Question field
            'validate': (is_required, is_string,),
        },
        'options': {  # Available answers
            'validate': (is_required, is_list, (has_min_length, 1)),
            'embed_many': {
                'value': {
                    'validate': (is_required, is_string,),
                },
                'correct': {
                    'validate': (is_required, is_boolean,),
                    'access': ('view',),
                },
                'feedback': {
                    'validate': (is_required, is_string,),
                    'access': ('view',),
                },
            }
        },
        'order': {
            'validate': (is_string, (is_one_of, 'random', 'set')),
            'default': 'random',
            'access': ('view',),
        },
        'max_options_to_show': {
            'validate': (is_integer,),
            'default': 4,
            'access': ('view',),
        }
    })

    def __init__(self, fields=None):
        """
        Create a new choice card instance.
        """

        super().__init__(fields)
        self['kind'] = 'choice'

    def validate(self):
        """
        Overwrite validate method to check options.
        """

        errors = super().validate()
        if not errors:
            error = has_correct_options(self['options'])
            if error:
                errors.append(error)
        return errors

    def validate_response(self, response):
        """
        Ensure the given response body is valid,
        given the card information.
        """

        values = [opt['value'] for opt in self['options']]

        if response not in values:
            return [{'message': 'Value is not an option.'}]

        return []

    def score_response(self, response):
        """
        Score the given response.
        Returns the score and feedback.
        """

        for opt in self['options']:
            if response == opt['value']:
                if opt['correct']:
                    return 1.0, opt['feedback']
                else:
                    return 0.0, opt['feedback']

        return 0.0, 'Default error ajflsdvco'
