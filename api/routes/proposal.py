from flask import Blueprint, jsonify, request, abort
from models.proposal import Proposal
from flask.ext.login import current_user
from modules.util import parse_args
from modules.entity import get_latest_canonical, get_kind, create_entity

proposal = Blueprint('proposal', __name__, url_prefix='/api/proposals')


@proposal.route('/', methods=['GET'])
def list_proposals():
    """
    Search through the proposals given a query, filters, and sorting.
    Pagination also available.
    Parameters:
    - query: a query string for rich-text search
    - kind: the kind of entity to search for (set, card, unit)
    - language: the language of the proposal and entity
    - user_id: the user who created the proposal
    - kind: create, update, or delete
    - status: pending, blocked, accepted, declined
    - skip: for pagination
    - limit: for pagination
    - order: created, modified, kind, status
    """
    pass
    # TODO: outline function


@proposal.route('/<proposal_id>/', methods=['GET'])
def get_proposal(proposal_id):
    """
    Get specific information about a proposal.
    Include entity information.
    Include votes.
    """
    args = parse_args(request.args)

    # TODO: Pull up the proposal data

    # TODO: Pull up the proposal entity version

    # TODO: Pull up the proposal latest canonical version
    latest_canonical = get_latest_canonical(proposal.entity.kind,
                                            proposal.entity.entity_id)

    # TODO: If the proposal isn't based off the latest canonical, it's invalid

    # TODO: Make a diff between the latest canonical
    # ... and the proposal entity version

    # TODO: Return all the join proposal data to user


@proposal.route('/', methods=['POST'])
def create_proposal():
    """
    Create a new proposal.
    Also must include entity (card, unit, set) information.
    """
    if not current_user.is_authenticated():
        return abort(401)

    # Create a new entity version
    entity, errors = create_entity(request.json)

    if errors:
        return jsonify(errors=errors), 400

    # Create the proposal
    kind = get_kind(request.json)
    prop_data = request.json.proposal
    prop_data.entity = {
        'kind': kind,
        'entity_id': entity.entity_id,
        'id': entity.id
    }
    proposal, errors = Proposal.insert(prop_data)

    if errors:
        return jsonify(errors=errors), 400

    # Return the proposal and entity
    return jsonify(**{
        'proposal': proposal,
        kind: entity,
    })


@proposal.route('/<proposal_id>/', methods=['PUT', 'PATCH'])
def update_proposal(proposal_id):
    """
    Update a proposal.
    The only field that can be updated is the status.
    """
    if not current_user.is_authenticated():
        return abort(401)
    # TODO: outline function


@proposal.route('/<proposal_id>/votes/', methods=['GET'])
def get_votes(proposal_id):
    """
    Produces the listing of votes.
    Paginates.
    Parameters:
    - skip
    - limit
    """
    args = parse_args(request.args)

    # TODO: outline function


@proposal.route('/<proposal_id>/votes/', methods=['POST'])
def create_vote(proposal_id):
    """
    Creates a new vote.
    Must include agreement kind.
    """
    if not current_user.is_authenticated():
        return abort(401)

    # TODO: outline function

    # TODO: If a proposal has sufficient votes, move it to canonical
    # ... and close out any prior versions dependent


@proposal.route('/<proposal_id>/votes/<vote_id>/', methods=['PUT'])
def update_vote(proposal_id, vote_id):
    """
    Updates a specific vote.
    """
    if not current_user.is_authenticated():
        return abort(401)

    # TODO: outline function
