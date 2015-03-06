from flask import Blueprint, abort  # , jsonify, request
# from models.card import Card
from flask.ext.login import current_user

card_routes = Blueprint('card', __name__, url_prefix='/api/cards')


@card_routes.route('/<card_id>/', methods=['GET'])
def get_card(card_id):
    """
    Get a specific card given an ID. Show all relevant data, but
    not used for the learning interface.
    """
    pass

    # TODO model
    # TODO get unit data
    # TODO join through requires both ways
    # TODO list of topics
    # TODO list of versions
    # TODO sequencer data: learners, transit, guess, slip, difficulty


@card_routes.route('/<card_id>/learn/', methods=['GET'])
def learn_card(card_id):
    """TODO
    Render the card's data, ready for learning.
    """

    if not current_user.is_authenticated():
        return abort(401)

    # TODO for the menu, we must include...
    #      set: name and id
    #      unit: name, body, id
    #      card: name and id


@card_routes.route('/<card_id>/responses/', methods=['POST'])
def respond_to_card(card_id):
    """TODO
    Record and process a learner's response to a card.
    """

    if not current_user.is_authenticated():
        return abort(401)
