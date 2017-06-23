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
        return abort(401)
    params = extend({}, request['params'], {'user_id': current_user['id']})
    notices = list_notices(params, db_conn)
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
        return abort(401)
    notice = get_notice({'id': notice_id}, db_conn)
    if not notice:
        return abort(404)
    if notice['user_id'] != current_user['id']:
        return abort(403)
    if 'read' not in request['params']:
        errors = [{
            'name': 'read',
            'message': 'You must specify read or unread.',
        }]
    elif request['params'].get('read') is True:
        notice, errors = mark_notice_as_read(notice, db_conn)
    elif request['params'].get('read') is False:
        notice, errors = mark_notice_as_unread(notice, db_conn)
    if len(errors):
        return 400, {
            'errors': errors,
            'ref': 'qR4CBtcfcYfWDTqK9JOXXLhO',
        }
    return 200, {'notice': deliver_notice(notice, access='private')}
