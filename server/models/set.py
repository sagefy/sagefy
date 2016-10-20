import rethinkdb as r
from modules.model import Model
from models.mixins.entity import EntityMixin
from models.unit import Unit
from modules.validations import is_required, is_string, is_list, is_one_of, \
    has_min_length
from modules.memoize_redis import memoize_redis
from models.set_parameters import SetParameters


class Set(EntityMixin, Model):
    """
    A set is a collection of units and other sets.
    Sets can vary greatly in scale.
    A graph is automatically formed based on the units and sets specified.
    """
    tablename = 'sets'

    parametersCls = SetParameters

    schema = dict(EntityMixin.schema.copy(), **{
        'body': {
            'validate': (is_required, is_string, (has_min_length, 1),)
        },
        'members': {
            'validate': (is_required, is_list, (has_min_length, 1)),
            'embed_many': {
                'id': {
                    'validate': (is_required, is_string,),
                },
                'kind': {
                    'validate': (is_required, is_string, (
                        is_one_of, 'unit', 'set'
                    )),
                }
            }
        }
    })

    def validate(self, db_conn):
        errors = super().validate(db_conn)
        if not errors:
            errors += self.is_valid_members(db_conn)
        if not errors:
            errors += self.ensure_no_cycles(db_conn)
        return errors

    def is_valid_members(self, db_conn):
        """

        """

        # TODO-3 this is going to be slow
        for member_desc in self['members']:
            query = (r.table(member_desc['kind'] + 's')
                      .filter(r.row['status'].eq('accepted'))
                      .filter(r.row['entity_id'] == member_desc['id']))
            vs = [e for e in query.run(db_conn)]
            if not vs:
                return [{
                    'message': 'Not a valid entity.',
                    'value': member_desc['id'],
                }]

        return []

    def ensure_no_cycles(self, db_conn):
        """
        Ensure no membership cycles form.
        """
        seen = set()
        main_id = self['entity_id']
        found = {'cycle': False}

        def _(members):
            if found['cycle']:
                return
            entity_ids = [
                member['id']
                for member in members
                if member['kind'] == 'set'
            ]
            entities = Set.list_by_entity_ids(db_conn, entity_ids)
            for entity in entities:
                if entity['entity_id'] == main_id:
                    found['cycle'] = True
                    break
                if entity['entity_id'] not in seen:
                    seen.add(entity['entity_id'])
                    _(entity['members'])

        _(self['members'])

        if found['cycle']:
            return [{'message': 'Found a cycle in membership.'}]

        return []

    @classmethod
    def get_all(cls, db_conn, limit=10, skip=0, **params):
        query = (cls.start_accepted_query()
                    .order_by(r.desc('created'))
                    .skip(skip)
                    .limit(limit))
        return [cls(document) for document in query.run(db_conn)]

    @classmethod
    def list_by_unit_id(cls, db_conn, unit_id):
        """
        Get a list of sets which contain the given member ID. Recursive.

        # TODO-2 is there a way to simplify this method?
        """

        def _():
            # *** First, find the list of sets
            #     directly containing the member ID. ***

            query = (cls.start_accepted_query()
                        .filter(r.row['members'].contains(
                            lambda member: member['id'] == unit_id
                        )))
            sets = query.run(db_conn)

            # *** Second, find all the sets containing
            #     those sets... recursively. ***

            found_sets, all_sets = sets, []

            while found_sets:
                set_ids = {set_['entity_id'] for set_ in found_sets}
                all_sets += found_sets
                query = (cls.start_accepted_query()
                            .filter(r.row['members'].contains(
                                lambda member:
                                    r.expr(set_ids).contains(member['id'])
                            )))
                found_sets = query.run(db_conn)

            return all_sets

        key = 'list_sets_by_unit_id_{id}'.format(id=unit_id)
        return [Set(data) for data in memoize_redis(key, _)]

    def list_units(self, db_conn):
        """
        Get the list of units contained within the set. Recursive. Connecting.

        TODO-2 OMG break into smaller functions
        TODO-2 Should this method be part of the Unit class/module,
             as it returns units?
        """

        def _():
            # *** First, we need to break down
            #     the set into a list of known units. ***

            unit_ids = set()
            sets = [self]

            while sets:
                set_ids = set()
                for set_ in sets:
                    unit_ids.update({member['id']
                                     for member in set_.data.get('members')
                                     if member['kind'] == 'unit'})
                    set_ids.update({member['id']
                                    for member in set_.data.get('members')
                                    if member['kind'] == 'set'})
                sets = Set.list_by_entity_ids(db_conn, set_ids)

            # *** Second, we need to find all
            #     the required connecting units. ***

            next_grab, units, unit_requires = unit_ids, [], {}

            while next_grab:
                tier_units = Unit.list_by_entity_ids(db_conn, next_grab)
                units += tier_units
                next_grab = set()

                for unit in tier_units:
                    if 'require_ids' not in unit:
                        continue
                    unit_id = unit['entity_id']
                    require_ids = unit_requires[unit_id] = \
                        set(unit['require_ids'])
                    for require_id in require_ids:
                        if require_id in unit_ids:
                            ids = {unit_id}
                            while ids:
                                unit_ids.update(ids)
                                ids = {unit_id
                                       for unit_id, require_ids
                                       in unit_requires.items()
                                       if unit_id not in unit_ids
                                       and require_ids & ids}
                        elif require_id not in unit_requires:
                            next_grab.add(require_id)

            units = [unit.data
                     for unit in units
                     if unit['entity_id'] in unit_ids]

            return units

        # If we already have it stored, use that
        key = 'set_units_{id}'.format(id=self['entity_id'])
        return [Unit(data) for data in memoize_redis(key, _)]
