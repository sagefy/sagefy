import pytest

xfail = pytest.mark.xfail

import framework.routes as routes
import re
from framework.routes import get, post, put, delete, abort, \
    build_path_pattern, find_path


def test_get():
    """
    Expect to add a handler to GET.
    """

    start_ln = len(routes.routes['GET'])

    @get('/s/foo')
    def foo_route(request):
        return 200, ''

    for path, fn in routes.routes['GET']:
        if fn == foo_route:
            found = (path, fn)
    assert found
    routes.routes['GET'].remove(found)
    assert len(routes.routes['GET']) == start_ln


def test_post():
    """
    Expect to add a handler to POST.
    """

    start_ln = len(routes.routes['POST'])

    @post('/s/foo')
    def foo_route(request):
        return 200, ''

    for path, fn in routes.routes['POST']:
        if fn == foo_route:
            found = (path, fn)
    assert found
    routes.routes['POST'].remove(found)
    assert len(routes.routes['POST']) == start_ln


def test_put():
    """
    Expect to add a handler to PUT.
    """

    start_ln = len(routes.routes['PUT'])

    @put('/s/foo')
    def foo_route(request):
        return 200, ''

    for path, fn in routes.routes['PUT']:
        if fn == foo_route:
            found = (path, fn)
    assert found
    routes.routes['PUT'].remove(found)
    assert len(routes.routes['PUT']) == start_ln


def test_delete():
    """
    Expect to add a handler to DELETE.
    """

    start_ln = len(routes.routes['DELETE'])

    @delete('/s/foo')
    def foo_route(request):
        return 200, ''

    for path, fn in routes.routes['DELETE']:
        if fn == foo_route:
            found = (path, fn)
    assert found
    routes.routes['DELETE'].remove(found)
    assert len(routes.routes['DELETE']) == start_ln


def test_build_path_pattern():
    """
    Expect to build a path pattern.
    """

    assert (build_path_pattern('/foo') ==
            re.compile('^/foo/?$'))
    assert (build_path_pattern('/foo/{u_id}') ==
            re.compile('^/foo/(?P<u_id>[\w\-]+)/?$'))
    assert (build_path_pattern('/foo/{u_id}/aaa/{n_id}') ==
            re.compile('^/foo/(?P<u_id>[\w\-]+)/aaa/(?P<n_id>[\w\-]+)/?$'))


def test_find_path():
    """
    Find a handler matching a path.
    """

    start_ln = len(routes.routes['GET'])

    @get('/s/foo/{u_id}')
    def foo_route(request):
        return 200, ''

    fn, params = find_path('GET', '/s/foo/a1')

    assert fn == foo_route
    assert params == {'u_id': 'a1'}

    path = re.compile('^/s/foo/(?P<u_id>[\w\-]+)/?$')
    routes.routes['GET'].remove((path, fn))
    assert len(routes.routes['GET']) == start_ln


def test_abort():
    """
    Expect to return a standard fail status.
    """

    code, response = abort(404)
    assert code == 404
    assert 'errors' in response
    assert response['errors'][0]['message'] == '404 Not Found'
