from flask import Blueprint, jsonify
docs = Blueprint('docs', __name__, url_prefix='/api/docs')


@docs.route('<page_slug>/')
def docs_page(page_slug):
    """
    View a documentation page.
    """
    return jsonify(**{})
