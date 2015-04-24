from framework.index import valuefy
import pytest

xfail = pytest.mark.xfail


@xfail
def test_serve():
    """
    Expect to handle a WSGI call.
    """

    assert False


@xfail
def test_call_handler():
    """
    Expect to call the handler matching the path.
    """

    assert False


@xfail
def test_construct_request():
    """
    Expect to contruct a request dictionary.
    """

    assert False


@xfail
def test_pull_query_string():
    """
    Expect to pull and format a query string.
    """

    assert False


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


@xfail
def test_pull_body():
    """
    Expect to pull and parse request body.
    """

    assert False


@xfail
def test_pull_cookies():
    """
    Expect to pull and format cookies.
    """

    assert False


@xfail
def test_pull_cookies_headers():
    """
    Expect to create headers to set cookies.
    """

    assert False


@xfail
def test_json_serial():
    """
    Expect to tell JSON how to format non-JSON types.
    """

    assert False
