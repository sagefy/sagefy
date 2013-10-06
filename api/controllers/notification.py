from app import app
from flask import jsonify


@app.route('/api/notifications/', methods=['GET'])
def list_notifications():
    """
    List notifications for current user.
    """
    return jsonify(**{})


@app.route('/api/notifications/', methods=['POST'])
def create_notifications():
    """
    Create a new notification.
    """
    return jsonify(**{})
