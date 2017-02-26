from modules.model import Model
from models.mixins.entity import EntityMixin
from modules.validations import is_required, is_string, is_list, \
    has_min_length


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

    schema = dict(EntityMixin.schema.copy(), **{
        'body': {
            'validate': (is_required, is_string, (has_min_length, 1),)
        },
        'require_ids': {
            'validate': (is_list,),
            'default': []
        },
    })

    def validate(self, db_conn):
        """

        """

        errors = super().validate(db_conn)
        if not errors:
            errors += self.ensure_requires(db_conn)
        if not errors:
            errors += self.ensure_no_cycles(db_conn)
        return errors

    def ensure_requires(self, db_conn):
        """

        """

        units = Unit.list_by_entity_ids(db_conn, self['require_ids'])
        if len(self['require_ids']) != len(units):
            return [{'message': 'Didn\'t find all requires.'}]
        return []

    def ensure_no_cycles(self, db_conn):
        """
        Ensure no require cycles form.
        """

        if self.find_requires_cycle(db_conn):
            return [{'message': 'Found a cycle in requires.'}]

        return []
