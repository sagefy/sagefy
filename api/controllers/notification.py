from flask import Blueprint
notification = Blueprint('notification', __name__,
                         url_prefix='/api/notifications')


@notification.route('/', methods=['GET'])
def list_notifications():
    """
    List notifications for current user.
    Takes parameters `limit`, `offset`, `categories`, and `read`.
    """


@notification.route('/<notification_id>/read',
                    methods=['PUT'])
def mark_notification_as_read(notification_id):
    """
    Marks notification as read.
    Must be logged in as user, provide a valid ID, and
    own the notification.
    Returns notification.
    """
