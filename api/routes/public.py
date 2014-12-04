from flask import Blueprint, jsonify
public = Blueprint('public', __name__, url_prefix='/api')
from modules.content import get as _


@public.route('/')
def api_index():
    """
    View a documentation page.
    """
    return jsonify(message=_('api', 'welcome'))
