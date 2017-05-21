# MMM
from framework.routes import get, abort
from database.topic import list_topics_by_entity_id, deliver_topic
from framework.session import get_current_user
from database.my_recently_created import get_my_recently_created_units
from database.entity_base import get_latest_accepted, get_versions, \
    list_requires, list_required_by


@get('/s/units/{unit_id}')
def get_unit_route(request, unit_id):
    """
    Get a specific unit given an ID.
    """

    db_conn = request['db_conn']

    unit = get_latest_accepted('units', db_conn, unit_id)
    if not unit:
        return abort(404)

    # TODO-2 SPLITUP create new endpoints for these instead
    topics = list_topics_by_entity_id(unit_id, {}, db_conn)
    versions = get_versions('units', db_conn, unit_id)
    requires = list_requires('units', db_conn, unit_id)
    required_by = list_required_by('units', db_conn, unit_id)
    subjects = Subject.list_by_unit_id(db_conn, unit_id)

    return 200, {
        'unit': unit.deliver(),
        # 'unit_parameters': unit.fetch_parameters(),
        'topics': [deliver_topic(topic) for topic in topics],
        'versions': [version.deliver() for version in versions],
        'requires': [require.deliver() for require in requires],
        'required_by': [require.deliver() for require in required_by],
        'belongs_to': [subject.deliver() for subject in subjects],
    }


@get('/s/units/{unit_id}/versions')
def get_unit_versions_route(request, unit_id):
    """
    Get unit versions given an ID. Paginates.
    """

    db_conn = request['db_conn']
    versions = get_versions(
        'units',
        db_conn,
        entity_id=unit_id,
        **request['params']
    )
    return 200, {
        'versions': [version.deliver(access='view') for version in versions]
    }


@get('/s/units:get_my_recently_created')
def get_my_recently_created_units_route(request):
    """
    Get the units the user most recently created.
    """

    current_user = get_current_user(request)
    if not current_user:
        return abort(401)
    db_conn = request['db_conn']
    units = get_my_recently_created_units(current_user, db_conn)
    return 200, {
        'units': [unit.deliver() for unit in units],
    }
