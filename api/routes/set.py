from flask import Blueprint, abort, jsonify
from models.set import Set
from models.topic import Topic
from flask.ext.login import current_user

# Nota Bene: We use `set_` because `set` is a type in Python
set_routes = Blueprint('set_', __name__, url_prefix='/api/sets')


@set_routes.route('/<set_id>/', methods=['GET'])
def get_set(set_id):
    """
    Get a specific set given an ID.
    """

    set_ = Set.get_latest_canonical(set_id)
    if not set_:
        return abort(404)

    topics = Topic.list_by_entity_id(entity_id=set_id)
    versions = Set.get_versions(entity_id=set_id)
    units = set_.list_units()

    return jsonify(
        set=set_.deliver(),
        topics=[topic.deliver() for topic in topics],
        versions=[version.deliver() for version in versions],
        units=[unit.deliver() for unit in units],
    )

    # TODO@ sequencer: learners, quality, difficulty


@set_routes.route('/<set_id>/versions/', methods=['GET'])
def get_set_versions(set_id):
    """
    Get versions set given an ID. Paginates.
    """

    # TODO@ add pagination
    versions = Set.get_versions(entity_id=set_id)
    return jsonify(versions=[version.deliver(access='view')
                             for version in versions])


@set_routes.route('/<set_id>/tree/', methods=['GET'])
def get_set_tree(set_id):
    """
    TODO@ Render the tree of units that exists within a set.
    """
    pass

    # Contexts:
    # - Search set, preview units in set
    # - Pre diagnosis
    # - Learner view progress in set
    # - Set complete

    # TODO@ For the menu, it must return the name and ID of the set


@set_routes.route('/<set_id>/units/', methods=['GET'])
def get_set_units(set_id):
    """
    TODO@ Render the units that exist within the set.
    Specifically, present a small number of units the learner can choose
    from.
    """

    if not current_user.is_authenticated():
        return abort(401)

    # TODO@ For the menu, it must return the name and ID of the set


@set_routes.route('/<set_id>/units/<unit_id>/', methods=['POST', 'PUT'])
def choose_unit(set_id, unit_id):
    """
    TODO@ Updates the learner's information based on the unit they have chosen.
    """

    if not current_user.is_authenticated():
        return abort(401)
