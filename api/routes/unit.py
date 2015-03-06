from flask import Blueprint, jsonify, request
from models.unit import Unit
from flask.ext.login import current_user

unit_routes = Blueprint('unit', __name__, url_prefix='/api/units')


@unit_routes.route('/<unit>/', methods=['GET'])
def get_unit(unit_id):
    """
    Get a specific unit given an ID.
    """
    pass

    # TODO provide model data
    # TODO join through requires
    # TODO join through sets
    # TODO list of topics
    # TODO list of versions
    # TODO sequencer data: learners, quality, difficulty
