from flask import Blueprint, jsonify, request
from models.set import Set
from flask.ext.login import current_user

set_ = Blueprint('set_', __name__, url_prefix='/api/sets')


@set_.route('/', methods=['GET'])
def list_sets():
    """
    Search the sets.
    Include query string, filters, sorting.
    Paginates.
    """
    pass


@set_.route('/<set_id>', methods=['GET'])
def get_set(set_id):
    """
    Gets a specific set given an ID.
    """
    pass
