from app import app


@app.route('/api/notifications/', methods=['GET'])
def list_notifications():
    """
    List notifications for current user.
    """
    pass


@app.route('/api/notifications/', methods=['POST'])
def create_notifications():
    """
    Create a new notification.
    """
    pass
