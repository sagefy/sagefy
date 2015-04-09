# Standard lib imports
import json
import re
from urllib.parse import unquote_plus
from http.cookies import SimpleCookie
from datetime import datetime, timedelta
from traceback import format_exc

# Own imports
from framework.status_codes import status_codes
from framework.database import make_db_connection, close_db_connection
from framework.routes import find_path, abort
import framework.database
import framework.mail


config = {
    'debug': False
}


def update_config(conf_):
    """
    Updates configs for various modules.
    """

    config.update(conf_)
    framework.database.config.update(conf_)
    framework.mail.config.update(conf_)


def serve(environ, start_response):
    """
    Handle a WSGI request and response.
    """

    make_db_connection()
    code, data = call_handler(environ)
    close_db_connection()
    response_headers = [('Content-Type', 'application/json; charset=utf-8')]
    response_headers += pull_cookies_headers(data.pop('cookies', {}))
    status = str(code) + ' ' + status_codes.get(code, 'Unknown')
    start_response(status, response_headers)
    body = json.dumps(data, default=json_serial, ensure_ascii=False).encode()
    return [body]


def call_handler(environ):
    """
    Given a WSGI environment,
    call the appropriate handler.
    Return a tuple of code (str), data (dict), and cookies (list).
    """

    method = environ['REQUEST_METHOD']
    if method not in ('GET', 'POST', 'PUT', 'DELETE'):
        return abort(405)

    path = environ['SCRIPT_NAME'] + environ['PATH_INFO']
    handler, parameters = find_path(method, path)
    if not handler:
        return abort(404)

    try:
        return handler(request=construct_request(environ), **parameters)

    except Exception as e:
        if config['debug']:
            return 500, {'errors': [{
                'message': str(e),
                'stack': format_exc()
            }]}
        return abort(500)


def construct_request(environ):
    """
    Produce a request `object`
    given a body (get), query string (put, post), and cookies.
    """

    method = environ['REQUEST_METHOD']
    request = {}
    if method == 'GET':
        request['params'] = pull_query_string(environ)
    elif method in ('PUT', 'POST'):
        request['params'] = pull_body(environ)
    request['cookies'] = pull_cookies(environ)
    return request


def pull_query_string(environ):
    """
    Pulls and formats query string out of the WSGI environment.
    """

    args = unquote_plus(environ.get('QUERY_STRING', ''))
    if not args:
        return {}

    def _(pair):
        pair = pair.split('=')
        if len(pair) == 2:
            return pair
        return pair[0], ''

    args = dict(map(_, args.split('&')))
    return {key: valuefy(value) for key, value in args.items()}


def valuefy(value):
    """
    Convert string representation into a native type.
    """

    if value == 'true':
        return True
    if value == 'false':
        return False
    if value == 'null':
        return None
    if re.match(r'^\d+$', value):
        return int(value)
    if re.match(r'^\d+\.\d+$', value):
        return float(value)
    return value


def pull_body(environ):
    """
    Pulls the body out of the WSGI environment.
    """

    try:
        content_length = int(environ.get('CONTENT_LENGTH', 0))
        body = environ['wsgi.input'].read(content_length)
        body = body.decode()
        return json.loads(body, strict=False)
    except:
        return {}


def pull_cookies(environ):
    """
    Pulls and formats cookies stored by user for domain.
    <http://pwp.stevecassidy.net/wsgi/cookies.html>
    """

    cookie = SimpleCookie(environ.get('HTTP_COOKIE', ''))
    return {key: morsel.value for key, morsel in cookie.items()}


def pull_cookies_headers(cookies):
    """
    Given a list of cookies... create the headers to set them.
    """

    expires = ((datetime.utcnow() + timedelta(weeks=2))
               .strftime('%a, %d-%b-%Y %H:%M:%S GMT'))
    return [
        ('Set-Cookie', '; '.join([
            '{key}={value}',
            'expires={expires}',
            'Path=/',
            'HttpOnly',
        ]).format(key=key, value=value, expires=expires))
        for key, value in cookies.items()
    ]


def json_serial(val):
    """
    Tell `json.dumps` how to convert non-JSON types.
    """

    if isinstance(val, datetime):
        return val.isoformat()
