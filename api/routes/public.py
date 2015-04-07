from flask import Blueprint, jsonify
from modules.content import get as c

public_routes = Blueprint('public', __name__, url_prefix='/api')


@public_routes.route('/')
def api_index():
    """
    View a documentation page.
    """

    return jsonify(message=c('api', 'welcome'))
