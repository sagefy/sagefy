from flask import Blueprint  # , jsonify, request
# from models.card import Card
# from flask.ext.login import current_user

card = Blueprint('card', __name__, url_prefix='/api/cards')


@card.route('/<card_id>/', methods=['GET'])
def get_card(card_id):
    """TODO
    Get a specific card given an ID. Show all relevant data, but
    not used for the learning interface.
    """
    pass


@card.route('/<card_id>/learn/', methods=['GET'])
def learn_card(card_id):
    """TODO
    Render the card's data, ready for learning.
    """
    pass


@card.route('/<card_id>/responses/', methods=['POST'])
def respond_to_card(card_id):
    """TODO
    Record and process a learner's response to a card.
    """
    pass
