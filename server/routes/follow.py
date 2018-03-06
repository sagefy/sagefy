from framework.routes import get, post, delete, abort
from framework.session import get_current_user
from database.follow import get_follow_by_id, list_follows_by_user, \
    insert_follow, \
    deliver_follow, delete_follow
from database.user import get_user


@get('/s/follows')
def get_follows_route(request):
  """
  Get a list of the users follows.
  """

  db_conn = request['db_conn']
  current_user = get_current_user(request)
  user_id = request['params'].get('user_id')
  if user_id:
    user = get_user(db_conn, {'id': user_id})
    if not user:
      return abort(404, 'sYkDuhNmReOrKyR0xsBmHg')
    if (user != current_user and
        user['settings']['view_follows'] != 'public'):
      return abort(403, 'FnH15Y3MRma6bU2gXqzjQQ')
  else:
    user = current_user
    if not user:
      return abort(401, 'YMC5rhI1TOCgUQu6jJeoQg')
  params = dict(**request['params'])
  params['user_id'] = user['id']
  follows = list_follows_by_user(db_conn, params)
  return 200, {
    'follows': [deliver_follow(follow, access='private')
                for follow in follows]
  }


@post('/s/follows')
def follow_route(request):
  """
  Follow a card, unit, or subject.
  """

  db_conn = request['db_conn']
  current_user = get_current_user(request)
  if not current_user:
    return abort(401, '0kW_gcpzQ7GomlCM28R8hw')
  follow_data = dict(**request['params'])
  follow_data['user_id'] = current_user['id']
  follow, errors = insert_follow(db_conn, follow_data)
  if errors:
    return 400, {
      'errors': errors,
      'ref': 'R4AAxO7PT7udr2huRHIbnA'
    }
  return 200, {'follow': deliver_follow(follow, access='private')}


@delete('/s/follows/{follow_id}')
def unfollow_route(request, follow_id):
  """
  Remove a follow. Must be current user's own follow.
  """

  db_conn = request['db_conn']
  current_user = get_current_user(request)
  if not current_user:
    return abort(401, 'iKrN2Ka3QcCFUDla1hzKZw')
  follow = get_follow_by_id(db_conn, follow_id)
  if not follow:
    return abort(404, 'G1DL33D1SZiqE9VK5ndijA')
  if follow['user_id'] != current_user['id']:
    return abort(403, 'LTXzAzF_QoGqKZnHRetRXw')
  errors = delete_follow(db_conn, follow_id)
  if errors:
    return 400, {
      'errors': errors,
      'ref': 'l32PmWmPSp6J4RXLzQph1A'
    }
  return 200, {}
