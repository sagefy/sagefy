import pytest

xfail = pytest.mark.xfail


@xfail
def test_match_body(app):
    """
    Expect a match card require a body.
    """

    assert False


@xfail
def test_match_options(app):
    """
    Expect a match card require a options.
    (value correct feedback)
    """

    assert False


@xfail
def test_match_default_feedback(app):
    """
    Expect a match card require a default feedback.
    """

    assert False


@xfail
def test_match_casing(app):
    """
    Expect a match card to allow case sensitivity.
    """

    assert False
