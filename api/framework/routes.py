import re
from framework.status_codes import status_codes


routes = {
    'GET': [],
    'POST': [],
    'PUT': [],
    'DELETE': [],
}


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


def abort(code):
    """
    A standardized way to abort
    """

    return code, {'errors': [{
        'message': str(code) + ' ' + status_codes.get(code, 'Unknown')
    }]}
