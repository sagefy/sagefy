from framework.routes import get, abort
from framework.session import get_current_user
from database.user import get_learning_context
from modules.util import convert_uuid_to_slug


@get('/s/next')
def next_route(request):
  """
  Tell the learner where to go next.
  TODO-3 should we move all `next` data from individual endpoints
       to this one, and have the UI call this endpoint each time
       to get the next state?
  """

  current_user = get_current_user(request)
  if not current_user:
    return abort(401)
  context = get_learning_context(current_user)
  # If 'next' action, return that,
  # else 'next' is GET Choose Subject
  if context.get('next'):
    return 200, {
      'next': context['next']
    }
  return 200, {
    'next': {
      'method': 'GET',
      'path': '/s/users/{user_id}/subjects'.format(
        user_id=convert_uuid_to_slug(current_user['id'])
      ),
    }
  }
