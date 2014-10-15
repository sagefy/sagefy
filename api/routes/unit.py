from flask import Blueprint, jsonify, request
from models.unit import Unit
from flask.ext.login import current_user

unit = Blueprint('unit', __name__, url_prefix='/api/units')


@unit.route('/', methods=['GET'])
def list_units():
    """
    Search the unit.
    Include query string, filters, sorting.
    Paginates.
    """
    pass


@unit.route('/<unit>/', methods=['GET'])
def get_unit(unit_id):
    """
    Gets a specific unit given an ID.
    """
    pass
