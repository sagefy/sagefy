import pytest

xfail = pytest.mark.xfail


@xfail
def test_formula_body(app):
    """
    Expect a formula card to require a body.
    """

    assert False


@xfail
def test_formula_options(app):
    """
    Expect a formula card to require options.
    (value, correct, feedback)
    """

    assert False


@xfail
def test_formula_variables(app):
    """
    Expect a formula card to require variables.
    """

    assert False


@xfail
def test_formula_range(app):
    """
    Expect a formula card to require a range.
    """

    assert False


@xfail
def test_formula_default_feedback(app):
    """
    Expect a formula card to require default feedback.
    """

    assert False
