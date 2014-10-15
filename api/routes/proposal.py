from flask import Blueprint, jsonify, request
from models.proposal import Proposal
from models.vote import Vote
from flask.ext.login import current_user

proposal = Blueprint('proposal', __name__, url_prefix='/api/proposals')


@proposal.route('/', methods=['GET'])
def list_proposals():
    """
    Search through the proposals given a query, filters, and sorting.
    Pagination also available.
    """
    pass


@proposal.route('/<proposal_id>/', methods=['GET'])
def get_proposal(proposal_id):
    """
    Get specific information about a proposal.
    Include entity information.
    Include votes.
    """
    pass


@proposal.route('/', methods=['POST'])
def create_proposal():
    """
    Create a new proposal.
    Also must include entity (card, unit, set) information.
    """
    pass


@proposal.route('/<proposal_id>/', methods=['PUT', 'PATCH'])
def update_proposal(proposal_id):
    """
    Update a proposal.
    The only field that can be updated is the status.
    """
    pass


@proposal.route('/<proposal_id>/votes/', methods=['GET'])
def get_votes(proposal_id):
    """
    Produces the listing of votes.
    Paginates.
    """
    pass


@proposal.route('/<proposal_id>/votes/', methods=['POST'])
def create_vote(proposal_id):
    """
    Creates a new vote.
    Must include agreement kind.
    """
    pass


@proposal.route('/<proposal_id>/votes/<vote_id>/', methods=['PUT'])
def update_vote(proposal_id, vote_id):
    """
    Updates a specific vote.
    """
    pass
