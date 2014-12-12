from flask import Blueprint  # , jsonify, request
# from models.card import Card
# from flask.ext.login import current_user

card = Blueprint('card', __name__, url_prefix='/api/cards')


@card.route('/<card_id>/', methods=['GET'])
def get_card(card_id):
    """
    Gets a specific card given an ID.
    """
    pass
