from modules.memoize_redis import memoize_redis
from database.unit import update_unit
from database.subject import update_subject
from database.card import update_card

# if something breaks the import loop, it would likely be one
# of these files:
from database.post import list_posts
from modules.notices import send_notices
from database.user import get_user

from database.card import get_card_version, list_latest_accepted_cards
from database.subject import list_subjects_by_unit_flat, \
    list_subject_parents, list_latest_accepted_subjects, \
    get_unit_version
from database.unit import list_latest_accepted_units, \
    get_subject_version


def get_entity_version(db_conn, kind, version_id):
    """

    """

    if kind == 'card':
        return get_card_version(db_conn, version_id)
    if kind == 'unit':
        return get_unit_version(db_conn, version_id)
    if kind == 'subject':
        return get_subject_version(db_conn, version_id)


def list_subjects_by_unit_recursive(db_conn, unit_id):
    """
    Get a list of subjects which contain the given member ID. Recursive.

    # TODO-2 is there a way to simplify this method?
    """

    def _():
        # *** First, find the list of subjects
        #     directly containing the member ID. ***

        subjects = list_subjects_by_unit_flat(db_conn, unit_id)

        # *** Second, find all the subjects containing
        #     those subjects... recursively. ***

        found_subjects, all_subjects = subjects, []

        while found_subjects:
            all_subjects += found_subjects
            subject_ids = {
                subject['entity_id']
                for subject in found_subjects
            }
            for subject_id in subject_ids:
                found_subjects += list_subject_parents(db_conn, subject_id)

        return all_subjects

    key = 'list_subjects_by_unit_id_{id}'.format(id=unit_id)
    return [data for data in memoize_redis(key, _)]


def list_units_in_subject_recursive(db_conn, main_subject):
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
            subjects = list_latest_accepted_subjects(db_conn, subject_ids)

        # *** Second, we need to find all
        #     the required connecting units. ***

        next_grab, units, unit_requires = unit_ids, [], {}

        while next_grab:
            tier_units = list_latest_accepted_units(db_conn, next_grab)
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
        entity_version = get_entity_version(db_conn, tablename, version_id)
        votes = list_posts({
            'kind': 'vote',
            'replies_to_id': proposal['id'],
        }, db_conn)
        changed, status = get_entity_status(entity_version['status'], votes)

        if changed:
            entity_version['status'] = status
            if entity_kind == 'card':
                update_card(db_conn, entity_version, {'status': status})
            elif entity_kind == 'unit':
                update_unit(db_conn, entity_version, {'status': status})
            elif entity_kind == 'subject':
                update_subject(db_conn, entity_version, {'status': status})
            user = get_user(db_conn, {'id': proposal['user_id']})
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


def find_requires_cycle(db_conn, tablename, data):
    """
    Inspect own requires to see if a cycle is formed.
    """

    assert tablename in ('cards', 'units')

    seen = set()
    main_id = data['entity_id']
    found = {'cycle': False}

    def _(require_ids):
        if found['cycle']:
            return
        if tablename == 'cards':
            entities = list_latest_accepted_cards(db_conn, require_ids)
        elif tablename == 'units':
            entities = list_latest_accepted_units(db_conn, require_ids)
        for entity in entities:
            if entity['entity_id'] == main_id:
                found['cycle'] = True
                break
            if entity['entity_id'] not in seen:
                seen.add(entity['entity_id'])
                if 'require_ids' in entity:
                    _(entity['require_ids'])

    _(data['require_ids'])

    return found['cycle']
