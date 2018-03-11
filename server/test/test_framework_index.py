# pylint: disable=no-self-use,too-few-public-methods
from framework.index import valuefy, serve, call_handler, construct_request, \
  pull_query_string, pull_body, pull_cookies, set_cookie_headers


def test_serve():
  """
  Expect to handle a WSGI call.
  """

  def start_response(status, headers):
    pass

  response = serve({
    'REQUEST_METHOD': 'GET',
    'SCRIPT_NAME': '/foo',
    'PATH_INFO': '',
  }, start_response)

  assert isinstance(response, list)
  assert isinstance(response[0], bytes)


def test_call_handler():
  """
  Expect to call the handler matching the path.
  """

  code, response = call_handler({
    'method': 'GET',
    'path': '/foo',
  })

  assert code == 404
  assert 'errors' in response


def test_call_handler_other():
  """
  Expect to call the handler matching the path.
  """

  code, response = call_handler({
    'method': 'WAFFLE',
    'path': '/foo',
  })

  assert code == 405
  assert 'errors' in response


def test_call_handler_real():
  """
  Expect to call the handler matching the path.
  """

  import routes.public  # pylint: disable=unused-variable

  code, _ = call_handler({
    'method': 'GET',
    'path': '/s/',
  })

  assert code == 200


def test_construct_request():
  """
  Expect to contruct a request dictionary.
  """

  request = construct_request({}, {
    'REQUEST_METHOD': 'WAFFLE',
    'PATH_INFO': '/waffle',
    'SCRIPT_NAME': '',
  })
  assert isinstance(request, dict)


def test_pull_query_string():
  """
  Expect to pull and format a query string.
  """

  assert pull_query_string({
    'QUERY_STRING': 'foo=1&bar=baz&maa'
  }) == {
    'foo': 1,
    'bar': 'baz',
    'maa': '',
  }


def test_valuefy():
  """
  Expect to take a dict of args, all strings, and convert to appropriate
  types.
  """

  assert valuefy('test') == 'test'
  assert valuefy('true') is True
  assert valuefy('false') is False
  assert valuefy('null') is None
  assert valuefy('56') == 56
  assert valuefy('3.14') == 3.14


def test_pull_body():
  """
  Expect to pull and parse request body.
  """

  class Input(object):
    def read(self, length):
      return b'{"foo":1}'

  assert pull_body({
    'CONTENT_LENGTH': 9,
    'wsgi.input': Input()
  }) == {
    'foo': 1,
  }


def test_pull_body_fail():
  """
  Expect to default to empty body
  """

  class Input(object):
    def read(self, length):
      return None

  assert pull_body({
    'CONTENT_LENGTH': 9,
    'wsgi.input': Input()
  }) == {}


def test_pull_cookies():
  """
  Expect to pull and format cookies.
  """

  assert pull_cookies({
    'HTTP_COOKIE': 'theme=light',
  }) == {
    'theme': 'light',
  }


def test_set_cookie_headers():
  """
  Expect to create headers to set cookies.
  """

  headers = set_cookie_headers({'theme': 'light'})
  assert isinstance(headers, list)
  assert headers[0][0] == 'Set-Cookie'
  assert 'theme=light' in headers[0][1]
  assert 'Path=/' in headers[0][1]
  assert 'HttpOnly' in headers[0][1]
