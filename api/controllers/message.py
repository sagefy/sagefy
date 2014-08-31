from flask import Blueprint, jsonify, request
from models.message import Message
from flask.ext.login import current_user
message = Blueprint('message', __name__, url_prefix='/api/messages')


@message.route('/', methods=['GET'])
def list_messages():
    """
    - List messages
        - to user
        - from user
        - unread to user
    - Pagination (limit, skip)
    - Filter by tags
    """
    if not current_user.is_authenticated():
        return jsonify(errors=[{"message": "Must login."}]), 401
    if current_user.id.get() not in (request.json.get('to_user_id'),
                                     request.json.get('from_user_id')):
        return jsonify(errors=[{"message": "Not own message."}]), 403
    messages = Message.list(**request.json)
    return jsonify(messages=[m.deliver(private=True) for m in messages])


@message.route('/<message_id>', methods=['GET'])
def get_message(message_id):
    """
    Get message by ID.
    Must be either the `from` user or `to` user.
    """
    if not current_user.is_authenticated():
        return jsonify(errors=[{"message": "Must login."}]), 401
    message = Message.get(id=message_id)
    if not message:
        return jsonify(errors=[{"message": "No message found."}]), 404
    if current_user.id.get() not in (message.from_user_id.get(),
                                     message.to_user_id.get()):
        return jsonify(errors=[{"message": "Not own message."}]), 403
    return jsonify(message=message.deliver(private=True))


@message.route('/<message_id>/read', methods=['PUT'])
def read_message(message_id):
    """
    Set message mark as read.
    Must be `to` user.
    """
    if not current_user.is_authenticated():
        return jsonify(errors=[{"message": "Must login."}]), 401
    message = Message.get(id=message_id)
    if not message:
        return jsonify(errors=[{"message": "No message found."}]), 404
    if current_user.id.get() != message.to_user_id.get():
        return jsonify(errors=[{"message": "Not own message."}]), 403
    message.mark_as_read()
    return jsonify(message=message.deliver(private=True))


@message.route('/', methods=['POST'])
def create_message():
    """
    Create a message.
    Will do as current logged in user.
    """
    if not current_user.is_authenticated():
        return jsonify(errors=[{"message": "Must login."}]), 401
    fields = request.json
    fields['from_user_id'] = current_user.id.get()
    message, errors = Message.insert(fields)
    if len(errors):
        return jsonify(errors=errors), 400
    return jsonify(message=message.deliver(private=True))
