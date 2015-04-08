# Standard lib imports
import json
import re
from urllib.parse import unquote_plus
from http.cookies import SimpleCookie
from datetime import datetime, timedelta
from traceback import format_exc

# Own imports
from framework.status_codes import status_codes


config = {
    'debug': False
}

routes = {
    'GET': [],
    'POST': [],
    'PUT': [],
    'DELETE': [],
}

error_handlers = []


def get(path):
    """
    Register a path and handler for a GET request.
    """

    def decorator(handler):
        routes['GET'].append((build_path_pattern(path), handler,))
        return handler
    return decorator


def post(path):
    """
    Register a path and handler for a POST request.
    """

    def decorator(handler):
        routes['POST'].append((build_path_pattern(path), handler,))
        return handler
    return decorator


def put(path):
    """
    Register a path and handler for a PUT request.
    """

    def decorator(handler):
        routes['PUT'].append((build_path_pattern(path), handler,))
        return handler
    return decorator


def delete(path):
    """
    Register a path and handler for a DELETE request.
    """

    def decorator(handler):
        routes['DELETE'].append((build_path_pattern(path), handler,))
        return handler
    return decorator


def abort(code):
    """
    A standardized way to abort
    """

    return code, {'errors': [{'message': status_codes.get(code, 'Unknown')}]}


def build_path_pattern(path):
    """
    Given a path description string,
    produce a regexp expression.
    """

    path = re.sub(r'\{(\w+)\}', r'(?P<\1>[\w\-]+)', path)
    return re.compile('^' + path + '/?$')


def find_path(method, path):
    """
    Given a method and a path,
    find the route that matches.
    """
    for pattern, handler in routes[method]:
        match = pattern.match(path)
        if match:
            return handler, match.groupdict()
    return None, None


def pull_body(environ):
    """
    Pulls the body out of the WSGI environment.
    """

    try:
        content_length = int(environ.get('CONTENT_LENGTH', 0))
        body = environ['wsgi.input'].read(content_length)
        body = body.decode()
        body = json.loads(body, strict=False)
    except:
        body = {}
    return body


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


def pull_cookies(environ):
    """
    Pulls and formats cookies stored by user for domain.
    <http://pwp.stevecassidy.net/wsgi/cookies.html>
    """

    cookie = SimpleCookie(environ.get('HTTP_COOKIE', ''))
    return {key: morsel.value for key, morsel in cookie.items()}


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


def call_handler(environ):
    """
    Given a WSGI environment,
    call the appropriate handler.
    Return a tuple of code (str), data (dict), and cookies (list).
    """

    try:
        method = environ['REQUEST_METHOD']
        if method not in ('GET', 'POST', 'PUT', 'DELETE'):
            return abort(405)

        path = environ['SCRIPT_NAME'] + environ['PATH_INFO']
        handler, parameters = find_path(method, path)
        if not handler:
            return abort(404)

        return handler(request=construct_request(environ), **parameters)

    except Exception as e:
        for error_handler in error_handlers:
            error_handler(e, format_exc())
        if config['debug']:
            return 500, {'errors': [{
                'message': str(e),
                'stack': format_exc()
            }]}
        return abort(500)


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
        ]).format(key=key, value=value, expires=expires))
        for key, value in cookies.items()
    ]


def serve(environ, start_response):
    """
    Handle a WSGI request and response.
    """

    code, data = call_handler(environ)
    response_headers = [('Content-Type', 'application/json; charset=utf-8')]
    response_headers += pull_cookies_headers(data.pop('cookies', {}))
    status = str(code) + ' ' + status_codes.get(code, '???')
    start_response(status, response_headers)
    body = json.dumps(data, ensure_ascii=False).encode()
    return [body]
