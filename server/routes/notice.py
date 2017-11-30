from framework.routes import get, put, abort
from framework.session import get_current_user
from database.notice import list_notices, mark_notice_as_read, \
    mark_notice_as_unread, get_notice, deliver_notice
from modules.util import extend


@get('/s/notices')
def list_notices_route(request):
  """
  List notices for current user.
  Take parameters `limit`, `skip`, `tag`, and `read`.
  """

  db_conn = request['db_conn']
  current_user = get_current_user(request)
  if not current_user:
    return abort(401, '9oMIw3V8S3WeaLf9IgbmaQ')
  params = extend({}, request['params'], {'user_id': current_user['id']})
  notices = list_notices(db_conn, params)
  output = {'notices': [deliver_notice(notice, access='private')
                        for notice in notices]}
  return 200, output


@put('/s/notices/{notice_id}')
def mark_notice_route(request, notice_id):
  """
  Mark notice as read or unread.
  Must be logged in as user, provide a valid ID, and own the notice.
  Return notice.
  """

  db_conn = request['db_conn']

  current_user = get_current_user(request)
  if not current_user:
    return abort(401, 'EWoueZr0TYSccUhdNISK3A')
  notice = get_notice(db_conn, {'id': notice_id})
  if not notice:
    return abort(404, 'xsNPOqJoRw-aUrFo0RhVoA')
  if notice['user_id'] != current_user['id']:
    return abort(403, 'xPkb7MYXRIOaI7HeV9U37A')
  if 'read' not in request['params']:
    errors = [{
      'name': 'read',
      'message': 'You must specify read or unread.',
      'ref': 'bvtS4G4jQnaLlVSLyUXjVg',
    }]
  elif request['params'].get('read') is True:
    notice, errors = mark_notice_as_read(db_conn, notice)
  elif request['params'].get('read') is False:
    notice, errors = mark_notice_as_unread(db_conn, notice)
  if errors:
    return 400, {
      'errors': errors,
      'ref': 'FeEtTWJJQv22dTpz8y5fZA',
    }
  return 200, {'notice': deliver_notice(notice, access='private')}
