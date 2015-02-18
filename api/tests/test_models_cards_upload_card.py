import pytest

xfail = pytest.mark.xfail


@xfail
def test_upload_body(app):
    """
    Expect an upload card to require a body.
    """

    assert False


@xfail
def test_upload_file_extensions(app):
    """
    Expect an upload card to require file_extensions.
    """

    assert False


@xfail
def test_upload_rubric(app):
    """
    Expect an upload card to require a rubric.
    """

    assert False
