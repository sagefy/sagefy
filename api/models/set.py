from flask import g
import rethinkdb as r
from modules.model import Model
from models.mixins.entity import EntityMixin
from models.unit import Unit
from modules.validations import is_required, is_language, is_string, \
    is_boolean, is_list, is_entity_list_dict
from modules.util import uniqid


# TODO@ On set canonical, index (or delete) in Elasticsearch with entity_id
class Set(EntityMixin, Model):
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
        'canonical': {
            'validate': (is_boolean,),
            'default': False
        },
        'available': {
            'validate': (is_boolean,),
            'default': True
        },
        'tags': {
            'validate': (is_list,),
            'default': []
        },
        'members': {
            'validate': (is_required, is_entity_list_dict,),
            # TODO@ is valid ids?
        }
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

    @classmethod
    def list_by_unit_id(cls, unit_id):
        """
        Get a list of sets which contain the given member ID. Recursive.
        """

        # *** First, find the list of sets
        #     directly containing the member ID. ***

        query = (cls.start_canonicals_query()
                    .filter(r.row['members'].contains({
                        'kind': 'unit',
                        'id': unit_id,
                    })))
        all_sets = query.run(g.db_conn)

        # *** Second, find all the sets containing
        #     those sets... recursively. ***

        set_ids = [set_['entity_id'] for set_ in all_sets]

        def find_sets_containing_set_ids(set_ids):
            query = (cls.start_canonicals_query()
                        .filter(r.row['members'].contains({
                            'kind': 'set',
                            'id': set_ids,  # TODO@
                        })))
            found_sets = query.run(g.db_conn)
            if len(found_sets) > 0:
                set_ids = set(set_['entity_id'] for set_ in found_sets)
                all_sets.concat(found_sets)
                find_sets_containing_set_ids(set_ids)

        find_sets_containing_set_ids(set_ids)

        return all_sets

    def list_units(self):
        """
        Get the list of units contained within the set. Recursive. Connecting.
        """

        # *** First, we need to break down
        #     the set into a list of known units. ***

        unit_ids = set()

        def break_down_sets(sets):
            set_ids = set()
            for set_ in sets:
                unit_ids.update(set(member['id']
                                    for member in getattr(set_, 'members', ())
                                    if member['kind'] == 'unit'))
                set_ids.update(set(member['id']
                                   for member in getattr(set_, 'members', ())
                                   if member['kind'] == 'set'))
            if len(set_ids) > 0:
                sets = Set.list_by_entity_ids(entity_ids=set_ids)
                break_down_sets(sets)

        break_down_sets([self])

        # *** Second, we need to find all
        #     the required connecting units. ***

        grabbed_units = []
        unit_requires = {}

        def connect(ids):
            unit_ids.update(ids)
            next = set(unit_id
                       for unit_id, require_ids in unit_requires.items()
                       if unit_id not in unit_ids and require_ids & ids)
            connect(next)

        def find_connections(given_unit_ids):
            units = Unit.list_by_entity_ids(given_unit_ids)
            grabbed_units.concat(units)
            next_grab = set()

            for unit in units:
                if 'require_ids' not in unit:
                    continue
                unit_id = unit['entity_id']
                require_ids = unit_requires[unit_id] = set(unit['require_ids'])
                for require_id in require_ids:
                    if require_id in unit_ids:
                        connect({unit_id})
                    elif require_id not in unit_requires:
                        next_grab.add(require_id)

            if len(next_grab) > 0:
                find_connections(next_grab)

        find_connections(unit_ids)

        return [unit
                for unit in grabbed_units
                if unit['entity_id'] in unit_ids]
