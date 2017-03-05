from framework.routes import get, abort
from models.unit import Unit
from models.set import Set
from database.topic import list_topics_by_entity_id, deliver_topic


@get('/s/units/{unit_id}')
def get_unit_route(request, unit_id):
    """
    Get a specific unit given an ID.
    """

    db_conn = request['db_conn']

    unit = Unit.get_latest_accepted(db_conn, unit_id)
    if not unit:
        return abort(404)

    # TODO-2 SPLITUP create new endpoints for these instead
    topics = list_topics_by_entity_id(unit_id, {}, db_conn)
    versions = Unit.get_versions(db_conn, unit_id)
    requires = Unit.list_requires(db_conn, unit_id)
    required_by = Unit.list_required_by(db_conn, unit_id)
    sets = Set.list_by_unit_id(db_conn, unit_id)

    return 200, {
        'unit': unit.deliver(),
        # 'unit_parameters': unit.fetch_parameters(),
        'topics': [deliver_topic(topic) for topic in topics],
        'versions': [version.deliver() for version in versions],
        'requires': [require.deliver() for require in requires],
        'required_by': [require.deliver() for require in required_by],
        'belongs_to': [set_.deliver() for set_ in sets],
    }


@get('/s/units/{unit_id}/versions')
def get_unit_versions_route(request, unit_id):
    """
    Get unit versions given an ID. Paginates.
    """

    db_conn = request['db_conn']
    versions = Unit.get_versions(
        db_conn,
        entity_id=unit_id,
        **request['params']
    )
    return 200, {
        'versions': [version.deliver(access='view') for version in versions]
    }
