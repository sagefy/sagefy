from app import app


@app.route('/api/users/login/', methods=['POST'])
def login():
    """
    Login user.
    """
    pass


@app.route('/api/users/logout/', methods=['POST'])
def logout():
    """
    Logout user.
    """
    pass


@app.route('/api/users/current/', methods=['GET'])
def get_current_user():
    """
    Get current user's information.
    """
    pass


@app.route('/api/users/<user_id>/', methods=['GET'])
def get_user_by_id(user_id):
    """
    Get user by ID.
    """
    pass


@app.route('/api/users/', methods=['POST'])
def create_user(user_id):
    """
    Create user.
    """
    pass


@app.route('/api/users/<user_id>/', methods=['POST'])
def update_user(user_id):
    """
    Update user.
    """
    pass


@app.route('/api/users/create_password/', methods=['POST'])
def create_password():
    """
    Create password.
    """
    pass
