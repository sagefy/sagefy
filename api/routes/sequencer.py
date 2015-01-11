from flask import Blueprint

sequencer = Blueprint('sequencer', __name__, url_prefix='/api/sequencer')


@sequencer.route('/next/', methods=['GET'])
def next():
    """
    Tells the learner where to go next.
    """
    pass
