from flask import Blueprint, abort, jsonify
from flask.ext.login import current_user
from models.card import Card
from models.unit import Unit
from models.topic import Topic
from models.response import Response
from modules.util import pick


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

    # TODO@ 400: Does the card make sense, given the context?

    # TODO@ for the menu, we must include...
    #      [ ] set: name and id  (context)
    #      [ ] unit: name, body, id  (context)
    #      [x] card: name and id

    # TODO@ return a limited set

    return jsonify(
        card=card.deliver(access=''),
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

    # TODO@ 400a Does the card make sense, given the context?

    # TODO@ 400b Is the response valid?

    return '', 204
