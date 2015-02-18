import pytest

xfail = pytest.mark.xfail


@xfail
def test_slideshow_site(app):
    """
    Expect a slideshow card to require a site.
    """

    assert False


@xfail
def test_slideshow_id(app):
    """
    Expect a slideshow card to require a slideshow_id.
    """

    assert False
