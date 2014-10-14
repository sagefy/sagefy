from flask import jsonify
from modules.content import get as _
from werkzeug.exceptions import HTTPException


# A rather comprehensive list of error codes
# Most probably won't be used
messages = {
    400: _('error', 'code_400'),
    401: _('error', 'code_401'),
    402: 'Payment Required',
    403: _('error', 'code_403'),
    404: _('error', 'code_404'),
    405: _('error', 'code_405'),
    406: 'Not Acceptable',
    407: 'Proxy Authentication Required',
    408: 'Request Timeout',
    409: 'Conflict',
    410: 'Gone',
    411: 'Length Required',
    412: 'Precondition Failed',
    413: 'Request Entity Too Large',
    414: 'Request URI Too Large',
    415: 'Unsupported Media Type',
    416: 'Requested Range Not Satisfiable',
    417: 'Expectation Failed',
    418: 'Im A Teapot',
    419: 'Authentication Timeout',
    420: 'Enhance Your Calm',
    422: 'Unprocessable Entity',
    424: 'Failed Dependency',
    425: 'Unordered Collection',
    426: 'Upgrade Required',
    428: 'Precondition Required',
    429: 'Too Many Requests',
    431: 'Request Header Fields Too Large',
    444: 'No Response',
    500: _('error', 'code_500'),
    501: 'Not Implemented',
    502: _('error', 'code_502'),
    503: _('error', 'code_503'),
    504: 'Gateway Timeout',
    505: 'Version Not Supported',
    506: 'Variant Also Negotiates',
}


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
            'message': messages[code],
            'code': code,
        }]), code
    return fn


def setup_errors(app):
    """
    Given a Flask application instance,
    add error handling for each type of error code.
    """
    for code, message in messages.items():
        app.error_handler_spec[None][code] = error_response(code)
