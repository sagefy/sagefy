from framework.routes import get, abort
from models.unit import Unit
from models.set import Set
from models.topic import Topic


@get('/s/units/{unit_id}')
def get_unit_route(request, unit_id):
    """
    Get a specific unit given an ID.
    """

    unit = Unit.get_latest_accepted(unit_id)
    if not unit:
        return abort(404)

    topics = Topic.list_by_entity_id(unit_id)
    versions = Unit.get_versions(unit_id)
    requires = Unit.list_requires(unit_id)
    required_by = Unit.list_required_by(unit_id)
    sets = Set.list_by_unit_id(unit_id)

    return 200, {
        'unit': unit.deliver(),
        'unit_parameters': unit.fetch_parameters(),
        'topics': [topic.deliver() for topic in topics],
        'versions': [version.deliver() for version in versions],
        'requires': [require.deliver() for require in requires],
        'required_by': [require.deliver() for require in required_by],
        'sets': [set_.deliver() for set_ in sets],
    }


@get('/s/units/{unit_id}/versions')
def get_unit_versions_route(request, unit_id):
    """
    Get unit versions given an ID. Paginates.
    """

    versions = Unit.get_versions(entity_id=unit_id, **request['params'])
    return 200, {
        'versions': [version.deliver(access='view') for version in versions]
    }
