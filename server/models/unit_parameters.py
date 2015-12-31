from modules.model import Model
from modules.validations import is_required, is_string


class UnitParameters(Model):
    tablename = 'units_parameters'

    schema = dict(Model.schema.copy(), **{
        'entity_id': {
            'validate': (is_required, is_string),  # TODO-1 validate foreign
        },
    })

    def get_learners(self):
        """

        """

    def get_difficulty(self):
        """

        """

    def get_quality(self):
        """

        """
