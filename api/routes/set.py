from flask import Blueprint
# , jsonify, request
# from models.set import Set
# from flask.ext.login import current_user

# We use `set_` because `set` is a type in Python
set_ = Blueprint('set_', __name__, url_prefix='/api/sets')


@set_.route('/<set_id>/', methods=['GET'])
def get_set(set_id):
    """
    Gets a specific set given an ID.
    """
    pass


@set_.route('/<set_id>/tree/', methods=['GET'])
def get_set_tree(set_id):
    """
    Renders the tree of units that exists within a set.
    """
    pass


@set_.route('/<set_id>/units/', methods=['GET'])
def get_set_units(set_id):
    """
    Renders the units that exist within the set.
    Specifically, presents a small number of units the learner can choose
    from.
    """
    pass


@set_.route('/<set_id>/units/<unit_id>/', methods=['POST', 'PUT'])
def choose_unit(set_id, unit_id):
    """
    Updates the learner's information based on the unit they have chosen.
    """
    pass
