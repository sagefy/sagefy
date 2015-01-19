from modules.model import Model
from modules.validations import is_required, is_string, is_number
from modules.content import get as _


def is_score(val):
    if not (0 <= val <= 1):
        return _('error', 'number')


class Response(Model):
    """
    Records the list of sets the learner has added.
    """
    tablename = 'responses'

    schema = dict(Model.schema.copy(), **{
        'user_id': {
            'validate': (is_required, is_string,),
        },
        'card_id': {
            'validate': (is_required, is_string,),
        },
        'unit_id': {
            'validate': (is_required, is_string,),
        },
        'score': {
            'validate': (is_required, is_number, is_score),
        }
    })
