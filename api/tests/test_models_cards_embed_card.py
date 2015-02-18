import pytest

xfail = pytest.mark.xfail


@xfail
def test_embed_url(app):
    """
    Expect embed card to require URL.
    """

    assert False


@xfail
def test_embed_rubric(app):
    """
    Expect embed card to require a rubric.
    """

    assert False
