from modules.model import Model
from modules.validations import is_required, is_string, is_list_of_strings


class UserSets(Model):
    """
    Records the list of sets the learner has added.
    """

    schema = dict(Model.schema.copy(), **{
        'user_id': {
            'validate': (is_required, is_string,),
        },
        'set_ids': {
            'validate': (is_required, is_list_of_strings,),
            'default': [],
        }
    })
