import pytest

xfail = pytest.mark.xfail


@xfail
def test_page_body(app):
    """
    Expect a page card to require a body.
    """

    assert False
