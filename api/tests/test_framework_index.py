from framework.index import valuefy
import pytest

xfail = pytest.mark.xfail

# TODO@ outline tests


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
