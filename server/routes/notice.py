from framework.routes import get, put, abort
from framework.session import get_current_user
from models.notice import Notice


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
    notices = Notice.list(db_conn,
                          user_id=current_user['id'],
                          **request['params'])
    output = {'notices': [notice.deliver(access='private')
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
    notice = Notice.get(db_conn, id=notice_id)
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
        notice, errors = notice.mark_as_read(db_conn)
    elif request['params'].get('read') is False:
        notice, errors = notice.mark_as_unread(db_conn)
    if len(errors):
        return 400, {
            'errors': errors,
            'ref': 'qR4CBtcfcYfWDTqK9JOXXLhO',
        }

    return 200, {'notice': notice.deliver(access='private')}
