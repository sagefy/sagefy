from flask import Blueprint, jsonify, request
from flask.ext.login import current_user
# from models.message import Message
message = Blueprint('message', __name__, url_prefix='/api/messages')


@message.route('/', methods=['GET'])
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


@message.route('/<message_id>/', methods=['GET'])
def get_message(message_id):
    """
    Get message
    """

    if not current_user:
        return jsonify(errors=[{
            "message": "You must be logged in to read a message."
        }]), 401

    return jsonify(**{})


@message.route('/', methods=['POST'])
def create_message():
    """
    Create message
    """

    if not current_user:
        return jsonify(errors=[{
            "message": "You must be logged in to create a message."
        }]), 401

    return jsonify(**{})
