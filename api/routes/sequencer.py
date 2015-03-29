from flask import Blueprint, abort, jsonify
from flask.ext.login import current_user
from modules.sequencer.index import main

sequencer_routes = Blueprint('sequencer',
                             __name__, url_prefix='/api/sequencer')


@sequencer_routes.route('/next/', methods=['GET'])
def next():
    """
    Tell the learner where to go next.
    """

    if not current_user.is_authenticated():
        return abort(401)

    context = current_user.get_learning_context()

    return jsonify(next=main(current_user['id'], context))   # TODO@ args
