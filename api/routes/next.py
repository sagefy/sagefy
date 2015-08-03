from framework.routes import get, abort
from framework.session import get_current_user


@get('/api/next')
def next_route(request):
    """
    Tell the learner where to go next.
    """

    current_user = get_current_user(request)
    if not current_user:
        return abort(401)

    context = current_user.get_learning_context()

    # If 'next' action, return that,
    # else 'next' is GET Choose Set
    if context.get('next'):
        return 200, {
            'next': context['next']
        }

    return 200, {
        'next': {
            'method': 'GET',
            'path': '/api/users/{user_id}/sets'
                    .format(user_id=current_user['id']),
        }
    }
