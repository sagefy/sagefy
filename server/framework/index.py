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
from modules.util import json_serial


config = {
    'debug': False,
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

    db_conn = make_db_connection()
    request = construct_request(db_conn, environ)
    code, data = call_handler(request)
    close_db_connection(db_conn)
    response_headers = [('Content-Type', 'application/json; charset=utf-8')]
    if isinstance(data, dict):
        response_headers += set_cookie_headers(data.pop('cookies', {}))
    status = str(code) + ' ' + status_codes.get(code, 'Unknown')
    start_response(status, response_headers)
    if isinstance(data, str):
        body = data.encode()
    elif isinstance(data, dict):
        body = json.dumps(data, default=json_serial, ensure_ascii=False)
        body = body.encode()
    return [body]


def construct_request(db_conn, environ):
    """
    Produce a request `object`
    given a body (get), query string (put, post), and cookies.
    """

    request = {}

    request['method'] = environ['REQUEST_METHOD']
    request['path'] = environ['SCRIPT_NAME'] + environ['PATH_INFO']
    request['db_conn'] = db_conn
    request['cookies'] = pull_cookies(environ)

    if request['method'] == 'GET':
        request['params'] = pull_query_string(environ)
    elif request['method'] in ('PUT', 'POST'):
        request['params'] = pull_body(environ)

    return request


def call_handler(request):
    """
    Given a request dictionary, call the appropriate handler.
    Return a tuple of code (str), data (dict), and cookies (list).
    """

    method = request['method']
    if method not in ('GET', 'POST', 'PUT', 'DELETE'):
        return abort(405)

    path = request['path']
    handler, parameters = find_path(method, path)
    if not handler:
        return abort(404)

    try:
        return handler(request=request, **parameters)

    except Exception:
        if config['debug']:
            return 500, format_exc()
        return abort(500)


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


def set_cookie_headers(cookies):
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
