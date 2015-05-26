from framework.routes import get, abort
from framework.session import get_current_user
from modules.sequencer.index import next


@get('/api/next')  # TODO@ get more RESTy
def next_route(request):
    """
    Tell the learner where to go next.
    """

    current_user = get_current_user(request)
    if not current_user:
        return abort(401)

    context = current_user.get_learning_context()

    # TODO@
    # GET Next
    #     -> Just in case, sends the next endpoint, or...
    #     -> GET Choose Set

    return 200, {
        'next': next(current_user, context)  # TODO@ args
    }
