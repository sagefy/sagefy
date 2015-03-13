from flask import Blueprint, jsonify, abort
from models.unit import Unit
from models.topic import Topic

unit_routes = Blueprint('unit', __name__, url_prefix='/api/units')


@unit_routes.route('/<unit_id>/', methods=['GET'])
def get_unit(unit_id):
    """
    Get a specific unit given an ID.
    """

    unit = Unit.get_latest_canonical(unit_id)
    if not unit:
        return abort(404)

    topics = Topic.list_by_entity_id(entity_id=unit_id)
    versions = Unit.get_versions(entity_id=unit_id)
    requires = Unit.list_requires(entity_id=unit_id)
    required_by = Unit.list_required_by(entity_id=unit_id)

    return jsonify(
        unit=unit.deliver(),
        topics=[topic.deliver() for topic in topics],
        versions=[version.deliver() for version in versions],
        requires=[require.deliver() for require in requires],
        required_by=[require.deliver() for require in required_by],
    )

    # TODO@ join through sets
    # TODO@ sequencer data: learners, quality, difficulty
