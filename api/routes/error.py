from flask import jsonify
from modules.content import get as _
from werkzeug.exceptions import HTTPException


# A rather comprehensive list of error codes
# Most probably won't be used
codes = (
    400,
    401,
    402,
    403,
    404,
    405,
    406,
    407,
    408,
    409,
    410,
    411,
    412,
    413,
    414,
    415,
    416,
    417,
    418,
    419,
    420,
    422,
    424,
    425,
    426,
    428,
    429,
    431,
    444,
    500,
    501,
    502,
    503,
    504,
    505,
    506,
)


def error_response(code):
    """
    A factory which produces controller functions
    for each type of error code.
    """
    def fn(error):
        if isinstance(error, HTTPException):
            code = error.code
        else:
            code = 500
        return jsonify(errors=[{
            'message': _('error', 'code_%s' % str(code)),
            'code': code,
        }]), code
    return fn


def setup_errors(app):
    """
    Given a Flask application instance,
    add error handling for each type of error code.
    """
    for code in codes:
        app.error_handler_spec[None][code] = error_response(code)
