import pytest

xfail = pytest.mark.xfail


@xfail
def test_get_latest_canonical(app, request):
    """
    Expect to pull the latest canonical
    version out of the database, given a kind and an entity_id.
    """

    return False


@xfail
def test_get_kind(json):
    """
    Expect to return kind as string given data.
    """

    return False


@xfail
def test_create_entity(json):
    """
    Expect to save a model to the DB given fields.
    """

    return False
