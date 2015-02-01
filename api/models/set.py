from modules.model import Model
from modules.validations import is_required, is_language, is_string, \
    is_boolean, is_list, is_entity_list_dict
from modules.util import uniqid
import rethinkdb as r
from flask import g


def ensure_no_cycles(value):
    """
    Ensure no membership cycles form.
    """
    # TODO


class Set(Model):
    """
    A set is a collection of units and other sets.
    Sets can vary greatly in scale.
    A graph is automatically formed based on the units and sets specified.
    """
    tablename = 'sets'

    """
    The model represents a **version** of a set, not a set itself.
    The `entity_id` attribute is what refers to a particular set.
    The `id` attribute refers to a specific version of the set.
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
        'members': {
            'validate': (is_required, is_entity_list_dict,
                         ensure_no_cycles)
        }
    })

    @classmethod
    def get_latest_canonical(cls, set_id):
        """
        Get the latest canonical version of the set.
        """

        if not set_id:
            return

        query = (cls.table
                    .filter(r.row['entity_id'] == set_id)
                    .order_by(r.desc('created'))
                    .limit(1))  # TODO this should have an index
        fields = list(query.run(g.db_conn))[0]

        if fields:
            return cls(fields)
