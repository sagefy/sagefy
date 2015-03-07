from flask import Blueprint, jsonify, abort
from models.unit import Unit

unit_routes = Blueprint('unit', __name__, url_prefix='/api/units')


@unit_routes.route('/<unit_id>/', methods=['GET'])
def get_unit(unit_id):
    """
    Get a specific unit given an ID.
    """

    unit = Unit.get_latest_canonical(unit_id)
    if not unit:
        return abort(404)

    return jsonify(
        unit=unit.deliver(),
    )

    # TODO provide model data
    # TODO join through requires
    # TODO join through sets
    # TODO list of topics
    # TODO list of versions
    # TODO sequencer data: learners, quality, difficulty
