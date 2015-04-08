from framework.index import get, abort
from framework.session import get_current_user
from modules.sequencer.index import main


@get('/api/sequencer/next')
def next_route(request):
    """
    Tell the learner where to go next.
    """

    current_user = get_current_user()
    if not current_user:
        return abort(401)

    context = current_user.get_learning_context()

    return 200, {
        'next': main(current_user['id'], context)  # TODO@ args
    }
