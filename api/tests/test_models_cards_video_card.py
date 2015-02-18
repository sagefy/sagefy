import pytest

xfail = pytest.mark.xfail


@xfail
def test_site(app):
    """
    Expect a video card to require a site.
    """

    assert False


@xfail
def test_video_id(app):
    """
    Expect a video card to require a video_id.
    """

    assert False
