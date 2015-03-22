from modules.model import Model
from modules.validations import is_required, is_string, is_number
from modules.content import get as c


def is_score(val):
    if val > 1 or val < 0:
        return c('error', 'number')


class Response(Model):
    """
    Record the list of sets the learner has added.
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
        'response': {
            'validate': (is_required,)
        },
        'score': {
            'validate': (is_required, is_number, is_score),
        }
    })
