import pytest

xfail = pytest.mark.xfail


@xfail
def test_choice_body(app):
    """
    Expect a choice card to require a body (question).
    """

    assert False


@xfail
def test_choice_options(app):
    """
    Expect a choice card to require a options (answers).
    (value, correct, feedback)
    """

    assert False


@xfail
def test_choice_order(app):
    """
    Expect a choice card to allow set order.
    """

    assert False


@xfail
def test_choice_max_opts(app):
    """
    Expect a choice card to allow max options (question).
    """

    assert False
