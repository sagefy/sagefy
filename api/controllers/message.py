from flask import Blueprint
message = Blueprint('message', __name__, url_prefix='/api/messages')


@message.route('/', methods=['GET'])
def list_messages():
    """
    - List messages
        - to user
        - from user
        - unread to user
    - Pagination (limit, offset)
    - Filter by categories
    """


@message.route('/<message_id>/', methods=['GET'])
def get_message(message_id):
    """
    Get message by ID.
    """


@message.route('/', methods=['POST'])
def create_message():
    """
    Create a message.
    """
