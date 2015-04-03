from modules.model import Model
from modules.validations import is_required, is_string


class SetParameters(Model):
    tablename = 'sets_parameters'

    schema = dict(Model.schema.copy(), **{
        'set_id': {
            'validate': (is_required, is_string),  # TODO@ validate foreign
        },
    })
