import pytest

xfail = pytest.mark.xfail


@xfail
def test_writing_body(app):
    """
    Expect writing card to require body.
    """

    assert False


@xfail
def test_writing_max_char(app):
    """
    Expect writing card to allow max char.
    """

    assert False


@xfail
def test_writing_rubric(app):
    """
    Expect writing card to require a rubric.
    """

    assert False
