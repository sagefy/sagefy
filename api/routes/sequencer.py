from flask import Blueprint, abort
from flask.ext.login import current_user

sequencer_routes = Blueprint('sequencer',
                             __name__, url_prefix='/api/sequencer')


@sequencer_routes.route('/next/', methods=['GET'])
def next():
    """TODO@
    Tell the learner where to go next.
    """

    if not current_user.is_authenticated():
        return abort(401)
