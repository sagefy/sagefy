from flask import Blueprint, jsonify, request
from flask.ext.login import current_user
from models.notification import Notification

notification = Blueprint('notification', __name__,
                         url_prefix='/api/notifications')


@notification.route('/', methods=['GET'])
def list_notifications():
    """
    List notifications for current user.
    Takes parameters `limit`, `skip`, `tag`, and `read`.
    """
    if not current_user.is_authenticated():
        return jsonify(errors=[{"message": "Must login."}]), 401
    notifications = Notification.list(user_id=current_user.id.get(),
                                      **request.json or {})
    return jsonify(notifications=[
        n.deliver(private=True)
        for n in notifications
    ])


@notification.route('/<notification_id>/read', methods=['PUT'])
def mark_notification_as_read(notification_id):
    """
    Marks notification as read.
    Must be logged in as user, provide a valid ID, and own the notification.
    Returns notification.
    """
    if not current_user.is_authenticated():
        return jsonify(errors=[{"message": "Must login."}]), 401
    notification = Notification.get(id=notification_id)
    if not notification:
        return jsonify(errors=[{"message": "Not found."}]), 404
    if notification.user_id.get() != current_user.id.get():
        return jsonify(errors=[{"message": "Not owned by user."}]), 403
    notification, errors = notification.mark_as_read()
    if len(errors):
        return jsonify(errors=errors), 400
    return jsonify(notification=notification.deliver(private=True))
