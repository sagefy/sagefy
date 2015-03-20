from flask import Blueprint, abort, jsonify, request
from flask.ext.login import current_user
from models.card import Card
from models.unit import Unit
from models.topic import Topic
from models.response import Response


card_routes = Blueprint('card', __name__, url_prefix='/api/cards')


@card_routes.route('/<card_id>/', methods=['GET'])
def get_card(card_id):
    """
    Get a specific card given an ID. Show all relevant data, but
    not used for the learning interface.
    """

    card = Card.get_latest_canonical(card_id)
    if not card:
        return abort(404)

    unit = Unit.get_latest_canonical(entity_id=card['unit_id'])
    if not unit:
        return abort(404)

    topics = Topic.list_by_entity_id(entity_id=card_id)
    versions = Card.get_versions(entity_id=card_id)
    requires = Card.list_requires(entity_id=card_id)
    required_by = Card.list_required_by(entity_id=card_id)

    return jsonify(
        card=card.deliver(access='view'),
        unit=unit.deliver(),
        topics=[topic.deliver() for topic in topics],
        versions=[version.deliver() for version in versions],
        requires=[require.deliver() for require in requires],
        required_by=[require.deliver() for require in required_by],
    )

    # TODO@ sequencer data: learners, transit, guess, slip, difficulty


@card_routes.route('/<card_id>/learn/', methods=['GET'])
def learn_card(card_id):
    """
    TODO@ Render the card's data, ready for learning.
    """

    if not current_user.is_authenticated():
        return abort(401)

    card = Card.get_latest_canonical(card_id)
    if not card:
        return abort(404)

    context = current_user.get_learning_context()
    if context.get('unit', {}).get('id') != card['unit_id']:
        return abort(400)

    current_user.set_learning_context(card=card)

    return jsonify(
        card=card.deliver(access=''),
        set=context.get('set'),
        unit=context.get('unit')
    )


@card_routes.route('/<card_id>/responses/', methods=['POST'])
def respond_to_card(card_id):
    """
    TODO@ Record and process a learner's response to a card.
    """

    if not current_user.is_authenticated():
        return abort(401)

    card = Card.get_latest_canonical(card_id)
    if not card:
        return abort(404)

    context = current_user.get_learning_context()
    if not context.get('card', {}).get('id') != card['entity_id']:
        return abort(400)

    errors = card.is_valid_response(request.json)
    if errors:
        return jsonify(errors=errors), 400

    response, errors = Response.insert(request.json)
    if errors:
        return jsonify(errors=errors), 400

    current_user.set_learning_context(card=None)

    return jsonify(response=response.deliver())
