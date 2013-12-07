from app import app
from flask import jsonify


@app.route('/api/docs/<page_slug>')
def docs_page():
    """
    View a documentation page.
    """
    return jsonify(**{})
