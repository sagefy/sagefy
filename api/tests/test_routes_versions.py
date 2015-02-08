import pytest

xfail = pytest.mark.xfail

# TODO this should probably be per entity type... unless there's
#      a way to make this a module


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
def test_version_canonical(app):
    """
    Expect to filter version by canonical.
    """
    assert False
