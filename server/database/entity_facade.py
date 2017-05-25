import rethinkdb as r
from modules.memoize_redis import memoize_redis
from modules.util import omit
from database.entity_base import list_by_entity_ids, get_version, \
    start_accepted_query
from database.unit import deliver_unit, update_unit
from database.subject import deliver_subject, update_subject
from database.card import deliver_card, update_card

# if something breaks the import loop, it would likely be one
# of these files:
from database.post import list_posts
from modules.notices import send_notices
from database.user import get_user


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


def list_subjects_by_unit_id(db_conn, unit_id):
    """
    Get a list of subjects which contain the given member ID. Recursive.

    # TODO-2 is there a way to simplify this method?
    """

    def _():
        # *** First, find the list of subjects
        #     directly containing the member ID. ***

        query = (start_accepted_query('subjects')
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
            query = (start_accepted_query('subjects')
                     .filter(r.row['members'].contains(
                         lambda member:
                             r.expr(subject_ids).contains(member['id'])
                     )))
            found_subjects = query.run(db_conn)

        return all_subjects

    key = 'list_subjects_by_unit_id_{id}'.format(id=unit_id)
    return [data for data in memoize_redis(key, _)]


def list_units_in_subject(main_subject, db_conn):
    """
    Get the list of units contained within the subject.
    Recursive. Connecting.

    TODO-2 OMG break into smaller functions
    """

    def _():
        # *** First, we need to break down
        #     the subject into a list of known units. ***

        unit_ids = set()
        subjects = [main_subject]

        while subjects:
            subject_ids = set()
            for subject in subjects:
                unit_ids.update({
                    member['id']
                    for member in subject.get('members')
                    if member['kind'] == 'unit'})
                subject_ids.update({
                    member['id']
                    for member in subject.get('members')
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
                    set(unit.get('require_ids'))
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

        units = [unit
                 for unit in units
                 if unit['entity_id'] in unit_ids]

        return units

    # If we already have it stored, use that
    key = 'subject_{id}'.format(id=main_subject['entity_id'])
    return [data for data in memoize_redis(key, _)]


def deliver_entity_by_kind(kind, entity):
    if kind == 'card':
        return deliver_card(entity, 'view')
    if kind == 'unit':
        return deliver_unit(entity, 'view')
    if kind == 'subject':
        return deliver_subject(entity, 'view')


def get_entity_status(current_status, votes):
    """
    Returns (changed, status) ... one of:
    (True, 'accepted|blocked|pending')
    (False, 'accepted|blocked|pending|declined')

    TODO-2 Update this to work as described in:
        http://docs.sagefy.org/Planning-Contributor-Ratings
        This requires knowing two things:
        - Number of learners the entity impacts
        - The vote and proposal history of the contributor
    """

    # Make sure the entity version status is not declined or accepted
    if current_status in ('accepted', 'declined'):
        return False, current_status
    # TODO-3 for now, we'll just accept all proposals as is
    # The algorithm should eventually be updated to match
    # https://docs.sagefy.org/Planning-Contributor-Ratings
    return True, 'accepted'


def update_entity_statuses(db_conn, proposal):
    """
    Update the entity's status based on the vote power received.
    Move to accepted or blocked if qualified.
    """

    # Get the entity version
    for p_entity_version in proposal['entity_versions']:
        entity_kind = p_entity_version['kind']
        version_id = p_entity_version['id']

        tablename = '%ss' % entity_kind
        entity_version = get_version(db_conn, tablename, version_id)
        votes = list_posts({
            'kind': 'vote',
            'replies_to_id': proposal['id'],
        }, db_conn)
        changed, status = get_entity_status(entity_version['status'], votes)

        if changed:
            entity_version['status'] = status
            if entity_kind == 'card':
                update_card(entity_version, {'status': status}, db_conn)
            elif entity_kind == 'unit':
                update_unit(entity_version, {'status': status}, db_conn)
            elif entity_kind == 'subject':
                update_subject(entity_version, {'status': status}, db_conn)
            user = get_user({'id': proposal['user_id']}, db_conn)
            send_notices(
                db_conn,
                entity_id=version_id,
                entity_kind=entity_kind,
                notice_kind=('block_proposal'
                             if status == 'blocked' else
                             'accept_proposal'),
                notice_data={
                    'user_name': user['name'],
                    'proposal_name': proposal['body'],
                    'entity_kind': entity_kind,
                    'entity_name': entity_version['name'],
                }
            )
