from database.post import list_posts
from models.unit import Unit
from models.subject import Subject


def get_my_recent_proposals(current_user, db_conn):
    """
    Gets a list of the user's most recent proposals.
    """

    return list_posts({
        'user_id': current_user['id'],
        'kind': 'proposal',
        'limit': 100,
    }, db_conn)


def get_proposal_entity_versions(proposals, kind):
    """
    Given a list of proposals and a kind,
    pull out all the entity ids matching that kind.
    """

    entity_ids = []
    for proposal in proposals:
        for entity_version in proposal['entity_versions']:
            if entity_version['kind'] == kind:
                entity_ids.append(entity_version['id'])
    return entity_ids


def get_my_recently_created_units(current_user, db_conn):
    """
    Get the user's most recently created units.
    """

    proposals = get_my_recent_proposals(current_user, db_conn)
    unit_version_ids = get_proposal_entity_versions(proposals, 'unit')
    units = Unit.list_by_version_ids(db_conn, unit_version_ids)
    return units


def get_my_recently_created_subjects(current_user, db_conn):
    """
    Get the user's most recently created subjects.
    """

    proposals = get_my_recent_proposals(current_user, db_conn)
    subject_version_ids = get_proposal_entity_versions(proposals, 'subject')
    subjects = Subject.list_by_version_ids(db_conn, subject_version_ids)
    return subjects
