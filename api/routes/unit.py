from flask import Blueprint, jsonify, request
from models.unit import Unit
from flask.ext.login import current_user

unit_routes = Blueprint('unit', __name__, url_prefix='/api/units')


@unit_routes.route('/<unit>/', methods=['GET'])
def get_unit(unit_id):
    """TODO
    Get a specific unit given an ID.
    """
    pass
