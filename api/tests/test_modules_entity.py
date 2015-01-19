# import rethinkdb as r
# from flask import g

import pytest

xfail = pytest.mark.xfail


@xfail
def test_get_latest_canonical(app, request):
    """
    Expect to pull the latest canonical
    version out of the database, given a kind and an entity_id.
    """

    assert False


@xfail
def test_get_kind(app, request):
    """
    Expect to return kind as string given data.
    """

    assert False


@xfail
def test_create_entity(app, request):
    """
    Expect to save a model to the DB given fields.
    """

    assert False
