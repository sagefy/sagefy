import pytest

xfail = pytest.mark.xfail


@xfail
def test_version(app):
    """
    Expect to filter to versions.
    """
    assert False


@xfail
def test_version_name(app):
    """
    Expect to search versions by proposal name.
    """
    assert False


@xfail
def test_version_entity(app):
    """
    Expect to filter versions by entity.
    """
    assert False


@xfail
def test_version_entity_kind(app):
    """
    Expect to filter versions by entity kind.
    """
    assert False


@xfail
def test_version_accepted(app):
    """
    Expect to filter version by accepted.
    """
    assert False
