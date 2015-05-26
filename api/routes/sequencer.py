from framework.routes import get, abort
from framework.session import get_current_user


@get('/api/next')  # TODO@ get more RESTy
def next_route(request):
    """
    Tell the learner where to go next.
    """

    current_user = get_current_user(request)
    if not current_user:
        return abort(401)

    context = current_user.get_learning_context()

    # If no 'next' action, next is GET Choose Set
    if 'next' not in context:
        return 200, {
            'next': {
                'path': '/api/users/{user_id}/sets'
                        .format(user_id=current_user['id']),
                'method': 'GET'
            }
        }

    return 200, {
        'next': context['next']
    }
