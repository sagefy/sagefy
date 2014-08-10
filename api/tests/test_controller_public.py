import pytest


@pytest.mark.xfail
def test_welcome(app):
    """
    Ensure the API returns a welcome message.
    """
    assert False
