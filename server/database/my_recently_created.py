from database.post import list_posts
from models.unit import Unit
from models.set import Set


def get_my_recent_proposals(current_user, db_conn):
    """
    Gets a list of the user's most recent proposals.
    """

    return list_posts({
        'user_id': current_user['id'],
        'kind': 'proposal',
        'limit': 100,
    }, db_conn)


def get_proposal_entities(proposals, kind):
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
    unit_ids = get_proposal_entities(proposals, 'unit')
    units = Unit.list_by_entity_ids(db_conn, unit_ids)
    return units


def get_my_recently_created_sets(current_user, db_conn):
    """
    Get the user's most recently created sets.
    """

    proposals = get_my_recent_proposals(current_user, db_conn)
    unit_ids = get_proposal_entities(proposals, 'set')
    sets = Set.list_by_entity_ids(db_conn, unit_ids)
    return sets
