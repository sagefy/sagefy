from app import app
from flask import jsonify
from flask import request
from flask.ext.login import current_user
# from models.message import Message


@app.route('/api/messages/', methods=['GET'])
def list_messages():
    """
    List messages
    - to user
    - from user
    - unread to user
    TODO: Pagination (limit, offset)
    TODO: Filter by category (categories[])
    """

    if not current_user:
        return jsonify(errors=[{
            "message": "You must be logged in to read messages."
        }]), 401

    if request.form.get('limit'):
        pass

    if request.form.get('categories'):
        pass

    return jsonify(**{})


@app.route('/api/messages/<message_id>/', methods=['GET'])
def get_message(message_id):
    """
    Get message
    """

    if not current_user:
        return jsonify(errors=[{
            "message": "You must be logged in to read a message."
        }]), 401

    return jsonify(**{})


@app.route('/api/messages/', methods=['POST'])
def create_message():
    """
    Create message
    """

    if not current_user:
        return jsonify(errors=[{
            "message": "You must be logged in to create a message."
        }]), 401

    return jsonify(**{})
