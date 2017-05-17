from modules.memoize_redis import memoize_redis
from modules.util import omit
import rethinkdb as r


def instance_entities(data):
    """
    Given a kind and some json, call insert on that kind
    and return the results.
    A little safer.
    """

    fields = ('id', 'created', 'modified',
              'entity_id', 'previous_id', 'status', 'available')
    entities = []
    if 'cards' in data:
        for card_data in data['cards']:
            entities.push(
                ('card', omit(card_data, fields))
            )
    if 'units' in data:
        entities = entities + [
            ('unit', omit(unit_data, fields))
            for unit_data in data['units']
        ]
    if 'subjects' in data:
        entities = entities + [
            ('subject', omit(subject_data, fields))
            for subject_data in data['subjects']
        ]
    return entities


def list_subjects_by_unit_id(cls, db_conn, unit_id):
    """
    Get a list of subjects which contain the given member ID. Recursive.

    # TODO-2 is there a way to simplify this method?
    """

    def _():
        # *** First, find the list of subjects
        #     directly containing the member ID. ***

        query = (cls.start_accepted_query()
                    .filter(r.row['members'].contains(
                        lambda member: member['id'] == unit_id
                    )))
        subjects = query.run(db_conn)

        # *** Second, find all the subjects containing
        #     those subjects... recursively. ***

        found_subjects, all_subjects = subjects, []

        while found_subjects:
            subject_ids = {
                subject['entity_id']
                for subject in found_subjects
            }
            all_subjects += found_subjects
            query = (cls.start_accepted_query()
                        .filter(r.row['members'].contains(
                            lambda member:
                                r.expr(subject_ids).contains(member['id'])
                        )))
            found_subjects = query.run(db_conn)

        return all_subjects

    key = 'list_subjects_by_unit_id_{id}'.format(id=unit_id)
    return [data for data in memoize_redis(key, _)]


def list_units_in_subject(self, db_conn):
    """
    Get the list of units contained within the subject.
    Recursive. Connecting.

    TODO-2 OMG break into smaller functions
    TODO-2 Should this method be part of the Unit class/module,
         as it returns units?
    """

    def _():
        # *** First, we need to break down
        #     the subject into a list of known units. ***

        unit_ids = set()
        subjects = [self]

        while subjects:
            subject_ids = set()
            for subject in subjects:
                unit_ids.update({
                    member['id']
                    for member in subject.data.get('members')
                    if member['kind'] == 'unit'})
                subject_ids.update({
                    member['id']
                    for member in subject.data.get('members')
                    if member['kind'] == 'subject'})
            subjects = list_by_entity_ids('subjects', db_conn, subject_ids)

        # *** Second, we need to find all
        #     the required connecting units. ***

        next_grab, units, unit_requires = unit_ids, [], {}

        while next_grab:
            tier_units = list_by_entity_ids('units', db_conn, next_grab)
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
    key = 'subject_{id}'.format(id=self['entity_id'])
    return [data for data in memoize_redis(key, _)]
