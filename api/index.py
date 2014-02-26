from app import app
from flask import jsonify
import controllers.user
import controllers.notification
import controllers.message


@app.route('/api/')
def api_index():
    """
    View a documentation page.
    """
    return jsonify(message='Welcome to the Sagefy API.')
