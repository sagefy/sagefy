import pytest

xfail = pytest.mark.xfail


@xfail
def test_get():
    """
    Expect to add a handler to GET.
    """

    assert False


@xfail
def test_post():
    """
    Expect to add a handler to POST.
    """

    assert False


@xfail
def test_put():
    """
    Expect to add a handler to PUT.
    """

    assert False


@xfail
def test_delete():
    """
    Expect to add a handler to DELETE.
    """

    assert False


@xfail
def test_build_path_pattern():
    """
    Expect to build a path pattern.
    """

    assert False


@xfail
def test_find_path():
    """
    Find a handler matching a path.
    """

    assert False


@xfail
def test_abort():
    """
    Expect to return a standard fail status.
    """

    assert False
