from modules.model import Model
from modules.validations import is_required, is_language, is_string, \
    is_boolean, is_list
from modules.util import uniqid
import rethinkdb as r
from flask import g


def ensure_no_cycles(value):
    """
    Ensure no require cycles form.
    """
    # TODO


class Unit(Model):
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
            'validate': (is_required, is_string,),
            'default': uniqid
        },
        'previous_id': {
            'validate': (is_string,),
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
        'canonical': {
            'validate': (is_boolean,),
            'default': False
        },
        'tags': {
            'validate': (is_list,),
            'default': []
        },
        'requires_ids': {
            'validate': (is_list, ensure_no_cycles),
            'default': []
        },
    })

    @classmethod
    def get_latest_canonical(cls, unit_id):
        """
        Get the latest canonical version of the unit.
        """

        if not unit_id:
            return

        query = (cls.table
                    .filter(r.row['entity_id'] == unit_id)
                    .order_by(r.desc('created'))
                    .limit(1))  # TODO this should have an index
        fields = list(query.run(g.db_conn))[0]

        if fields:
            return cls(fields)

    # TODO On set canonical, index in Elasticsearch with entity_id
