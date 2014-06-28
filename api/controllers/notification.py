from app import app
from flask import jsonify
# from models.notification import Notification
from flask import request
from flask.ext.login import current_user


@app.route('/api/notifications/', methods=['GET'])
def list_notifications():
    """
    List notifications for current user.
    TODO: Pagination (limit, offset, count)
    TODO: Filter by category (categories[])
    """

    if not current_user:
        return jsonify(errors=[{
            "message": "You must be logged in to read notifications."
        }]), 401

    if request.form.get('limit'):
        pass

    if request.form.get('categories'):
        pass

    return jsonify(notifications=[])
