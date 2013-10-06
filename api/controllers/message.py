from app import app


@app.route('/api/messages/', methods=['GET'])
def list_messages():
    """
    List messages
    - to user
    - from user
    - unread to user
    """
    pass


@app.route('/api/messages/<message_id>/', methods=['GET'])
def get_message(message_id):
    """
    Get message
    """
    pass


@app.route('/api/messages/', methods=['POST'])
def create_message():
    """
    Create message
    """
    pass
