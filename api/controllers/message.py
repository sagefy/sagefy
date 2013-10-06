from app import app
from flask import jsonify


@app.route('/api/messages/', methods=['GET'])
def list_messages():
    """
    List messages
    - to user
    - from user
    - unread to user
    """
    return jsonify(**{})


@app.route('/api/messages/<message_id>/', methods=['GET'])
def get_message(message_id):
    """
    Get message
    """
    return jsonify(**{})


@app.route('/api/messages/', methods=['POST'])
def create_message():
    """
    Create message
    """
    return jsonify(**{})
