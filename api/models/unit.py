from modules.model import Model
from models.mixins.entity import EntityMixin
from modules.validations import is_required, is_language, is_string, \
    is_boolean, is_list, is_list_of_strings
from modules.util import uniqid


# TODO@ On set accepted, index (or delete) in Elasticsearch with entity_id
class Unit(EntityMixin, Model):
    """
    A unit is the medium size in the Sagefy data structure system.
    A unit represents a unit of learning activity.
    A unit is defined by a single goal (objective). See Bloom’s Taxonomy.
    A unit should represent a goal that is as small as possible
    without becoming systemically redundant.
    An example of a unit is a small learning lesson,
    which may contain about five to eight minutes of information and
    30-60 minutes of practice to gain proficiency.
    """
    tablename = 'units'

    """
    The model represents a **version** of a unit, not a unit itself.
    The `entity_id` attribute is what refers to a particular unit.
    The `id` attribute refers to a specific version of the unit.
    The `previous_id` attribute refers to the version based off.
    """

    schema = dict(Model.schema.copy(), **{
        'entity_id': {
            'validate': (is_required, is_string,),  # TODO@ is valid id?
            'default': uniqid
        },
        'previous_id': {
            'validate': (is_string,),  # TODO@ is valid id?
        },
        'language': {
            'validate': (is_required, is_language,),
            'default': 'en'
        },
        'name': {
            'validate': (is_required, is_string,)
        },
        'body': {
            'validate': (is_required, is_string,)
        },
        'accepted': {
            'validate': (is_boolean,),
            'default': False
        },
        'available': {
            'validate': (is_boolean,),
            'default': True
        },
        'tags': {
            'validate': (is_list, is_list_of_strings),
            'default': []
        },
        'require_ids': {
            'validate': (is_list,),  # TODO@ is valid id?
            'default': []
        },
    })

    def validate(self):
        errors = super().validate()
        if not errors:
            errors += self.ensure_no_cycles()
        return errors

    def ensure_no_cycles(self):
        """
        TODO@ Ensure no require cycles form.
        """
        return []
