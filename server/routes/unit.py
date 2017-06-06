from framework.routes import get, post, abort
from database.topic import list_topics_by_entity_id, deliver_topic
from framework.session import get_current_user
from database.my_recently_created import get_my_recently_created_units
from database.entity_base import get_latest_accepted, get_versions, \
    list_requires, list_required_by, list_by_entity_ids, get_version
from database.entity_facade import list_subjects_by_unit_id
from database.unit import deliver_unit, insert_unit
from database.subject import deliver_subject
from copy import deepcopy
from modules.util import extend


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
    subjects = list_subjects_by_unit_id(db_conn, unit_id)

    return 200, {
        'unit': deliver_unit(unit),
        # TODO-3 unit parameters
        'topics': [deliver_topic(topic) for topic in topics],
        'versions': [deliver_unit(version) for version in versions],
        'requires': [deliver_unit(require) for require in requires],
        'required_by': [deliver_unit(require) for require in required_by],
        'belongs_to': [deliver_subject(subject) for subject in subjects],
    }


@get('/s/units')
def list_units_route(request):
    """
    Return a collection of units by `entity_id`.
    """

    db_conn = request['db_conn']
    entity_ids = request['params'].get('entity_ids')
    if not entity_ids:
        return abort(404)
    entity_ids = entity_ids.split(',')
    units = list_by_entity_ids('units', db_conn, entity_ids)
    if not units:
        return abort(404)
    return 200, {'units': [deliver_unit(unit, 'view') for unit in units]}


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
        'versions': [
            deliver_unit(version, access='view')
            for version in versions
        ]
    }


@get('/s/units/versions/{version_id}')
def get_unit_version_route(request, version_id):
    """
    Get a unit version only knowing the `version_id`.
    """

    db_conn = request['db_conn']
    unit_version = get_version(db_conn, 'units', version_id)
    if not unit_version:
        return abort(404)
    return 200, {'version': unit_version}


# TODO-1 move to /s/users/{user_id}/units (?)
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
        'units': [deliver_unit(unit) for unit in units],
    }


@post('/s/units/versions')
def create_new_unit_version_route(request):
    """
    Create a new unit version for a brand new unit.
    """

    current_user = get_current_user(request)
    if not current_user:
        return abort(401)
    db_conn = request['db_conn']
    data = deepcopy(request['params'])
    if 'entity_id' in data:
        return abort(403)
    data['user_id'] = current_user['id']
    unit, errors = insert_unit(db_conn, data)
    if len(errors):
        return 400, {
            'errors': errors,
            'ref': '9CuN9nYpmBXd45barbfoIe5t',
        }
    return 200, {'version': deliver_unit(unit, 'view')}


@post('/s/units/{unit_id}/versions')
def create_existing_unit_version_route(request, unit_id):
    """
    Create a new unit version for an existing unit.
    """

    current_user = get_current_user(request)
    if not current_user:
        return abort(401)
    db_conn = request['db_conn']
    next_data = deepcopy(request['params'])
    next_data['entity_id'] = unit_id
    next_data['user_id'] = current_user['id']
    current_unit = get_latest_accepted('units', db_conn, entity_id=unit_id)
    if not current_unit:
        return abort(404)
    unit_data = extend({}, current_unit, next_data)
    unit, errors = insert_unit(db_conn, unit_data)
    if len(errors):
        return 400, {
            'errors': errors,
            'ref': 'aint3EhS4LkTKuIoY0q07vHZ',
        }
    return 200, {'version': deliver_unit(unit, 'view')}
