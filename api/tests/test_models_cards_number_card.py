import pytest

xfail = pytest.mark.xfail


@xfail
def test_number_body(app):
    """
    Expect a number card to require a body.
    """

    assert False


@xfail
def test_number_options(app):
    """
    Expect a number card to require a options.
    (value correct feedback)
    """

    assert False


@xfail
def test_number_range(app):
    """
    Expect a number card to allow a range.
    """

    assert False


@xfail
def test_number_default_feedback(app):
    """
    Expect a number card to require default feedback.
    """

    assert False
