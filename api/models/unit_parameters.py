from modules.model import Model
from modules.validations import is_required, is_string


class UnitParameters(Model):
    tablename = 'units_parameters'

    schema = dict(Model.schema.copy(), **{
        'unit_id': {
            'validate': (is_required, is_string),  # TODO@ validate foreign
        },
    })
