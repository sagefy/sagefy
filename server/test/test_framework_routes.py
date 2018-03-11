# pylint: disable=anomalous-backslash-in-string
import re
from framework.routes import ROUTES
from framework.routes import get, post, put, delete, abort, \
  build_path_pattern, find_path


def test_get():
  """
  Expect to add a handler to GET.
  """

  start_ln = len(ROUTES['GET'])

  @get('/s/foo')
  def foo_route(request):
    return 200, ''

  for path, fn in ROUTES['GET']:
    if fn == foo_route:
      found = (path, fn)
  assert found
  ROUTES['GET'].remove(found)
  assert len(ROUTES['GET']) == start_ln


def test_post():
  """
  Expect to add a handler to POST.
  """

  start_ln = len(ROUTES['POST'])

  @post('/s/foo')
  def foo_route(request):
    return 200, ''

  for path, fn in ROUTES['POST']:
    if fn == foo_route:
      found = (path, fn)
  assert found
  ROUTES['POST'].remove(found)
  assert len(ROUTES['POST']) == start_ln


def test_put():
  """
  Expect to add a handler to PUT.
  """

  start_ln = len(ROUTES['PUT'])

  @put('/s/foo')
  def foo_route(request):
    return 200, ''

  for path, fn in ROUTES['PUT']:
    if fn == foo_route:
      found = (path, fn)
  assert found
  ROUTES['PUT'].remove(found)
  assert len(ROUTES['PUT']) == start_ln


def test_delete():
  """
  Expect to add a handler to DELETE.
  """

  start_ln = len(ROUTES['DELETE'])

  @delete('/s/foo')
  def foo_route(request):
    return 200, ''

  for path, fn in ROUTES['DELETE']:
    if fn == foo_route:
      found = (path, fn)
  assert found
  ROUTES['DELETE'].remove(found)
  assert len(ROUTES['DELETE']) == start_ln


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

  start_ln = len(ROUTES['GET'])

  @get('/s/foo/{u_id}')
  def foo_route(request):
    return 200, ''

  fn, params = find_path('GET', '/s/foo/a1')

  assert fn == foo_route
  assert params == {'u_id': 'a1'}

  path = re.compile('^/s/foo/(?P<u_id>[\w\-]+)/?$')
  ROUTES['GET'].remove((path, fn))
  assert len(ROUTES['GET']) == start_ln


def test_abort():
  """
  Expect to return a standard fail status.
  """

  code, response = abort(404)
  assert code == 404
  assert 'errors' in response
  assert response['errors'][0]['message'] == '404 Not Found'
