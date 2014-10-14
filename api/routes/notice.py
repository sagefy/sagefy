from flask import Blueprint, jsonify, request, abort
from flask.ext.login import current_user
from models.notice import Notice

notice = Blueprint('notice', __name__, url_prefix='/api/notices')


@notice.route('/', methods=['GET'])
def list_notices():
    """
    List notices for current user.
    Takes parameters `limit`, `skip`, `tag`, and `read`.
    """
    if not current_user.is_authenticated():
        return abort(401)
    notices = Notice.list(user_id=current_user.id, **request.args or {})
    return jsonify(notices=[
        n.deliver(private=True)
        for n in notices
    ])


@notice.route('/<notice_id>/read', methods=['PUT'])
def mark_notice_as_read(notice_id):
    """
    Marks notice as read.
    Must be logged in as user, provide a valid ID, and own the notice.
    Returns notice.
    """
    if not current_user.is_authenticated():
        return abort(401)
    notice = Notice.get(id=notice_id)
    if not notice:
        return abort(404)
    if notice.user_id != current_user.id:
        return abort(403)
    notice, errors = notice.mark_as_read()
    if len(errors):
        return jsonify(errors=errors), 400
    return jsonify(notice=notice.deliver(private=True))
