from flask import Blueprint, jsonify, request
from models.discuss.flag import Flag
from flask.ext.login import current_user

flag = Blueprint('flag', __name__, url_prefix='/api/flags')


@flag.route('/', methods=['POST'])
def flag():
    """
    Flag an entity.
    """
    pass
