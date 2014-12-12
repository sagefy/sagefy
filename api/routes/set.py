from flask import Blueprint
# , jsonify, request
# from models.set import Set
# from flask.ext.login import current_user

# We use `set_` because `set` is a type in Python
set_ = Blueprint('set_', __name__, url_prefix='/api/sets')


@set_.route('/<set_id>/', methods=['GET'])
def get_set(set_id):
    """
    Gets a specific set given an ID.
    """
    pass
