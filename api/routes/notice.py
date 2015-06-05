from framework.routes import get, put, abort
from framework.session import get_current_user
from models.notice import Notice


@get('/api/notices')
def list_notices_route(request):
    """
    List notices for current user.
    Take parameters `limit`, `skip`, `tag`, and `read`.
    """

    current_user = get_current_user(request)
    if not current_user:
        return abort(401)
    notices = Notice.list(user_id=current_user['id'], **request['params'])
    return 200, {'notices': [notice.deliver(access='private')
                             for notice in notices]}


@put('/api/notices/{notice_id}')
def mark_notice_route(request, notice_id):
    """
    Mark notice as read or unread.
    Must be logged in as user, provide a valid ID, and own the notice.
    Return notice.
    """

    current_user = get_current_user(request)
    if not current_user:
        return abort(401)
    notice = Notice.get(id=notice_id)
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
        notice, errors = notice.mark_as_read()
    elif request['params'].get('read') is False:
        notice, errors = notice.mark_as_unread()
    if len(errors):
        return 400, {'errors': errors}

    return 200, {'notice': notice.deliver(access='private')}
