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
        limit = int(request.values.get('limit') or 0)
        offset = int(request.values.get('offset') or 0)
        categories = request.values.get('categories') or []
        return jsonify(notifications=Notification.get_user_notifications(
            user_id=current_user.id,
            limit=limit,
            offset=offset,
            categories=categories
        ), limit=limit, offset=offset, categories=categories)
    except AssertionError as error:
        code = 400
        if error['name'] == 'user_id':
            code = 401
        return jsonify(errors=list(error)), code
