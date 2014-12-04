from flask import Blueprint, jsonify
public = Blueprint('public', __name__, url_prefix='/api')


@public.route('/')
def api_index():
    """
    View a documentation page.
    """
    return jsonify(message='Welcome to the Sagefy API.')
    # TODO: move copy to content directory
