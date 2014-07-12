from app import app
from flask import jsonify
from models.notification import Notification
from flask import request
from flask.ext.login import current_user


@app.route('/api/notifications/', methods=['GET'])
def list_notifications():
    """
    List notifications for current user.
    Takes parameters `limit`, `offset`, and `categories`.
    """

    try:
        limit = int(request.values.get('limit', 0))
        offset = int(request.values.get('offset', 0))
        categories = request.values.get('categories', [])
        read = request.values.get('read', None)
        return jsonify(notifications=Notification.get_user_notifications(
            user_id=current_user.id,
            limit=limit,
            offset=offset,
            categories=categories,
            read=read,
        ), parameters={
            'limit': limit,
            'offset': offset,
            'categories': categories,
            'read': read,
        })
    except AssertionError as error:
        code = 400
        if error['name'] == 'user_id':
            code = 401
        return jsonify(errors=list(error)), code


@app.route('/api/notifications/<notification_id>/read', methods=['PUT'])
def mark_notification_as_read(notification_id):
    """
    Marks notification as read.
    Must be logged in as user and provide a valid id.
    Returns notification.
    """

    notification = Notification.get_by_id(notification_id)
    if not notification:
        return jsonify(errors=[{'message': "Not a valid id."}]), 404
    if notification.user_id != current_user.id:
        return jsonify(errors=[{'message': "Not own notification."}]), 401
    notification.mark_as_read()
    return jsonify(notification=notification)
