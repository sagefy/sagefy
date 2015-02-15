import pytest

xfail = pytest.mark.xfail

import rethinkdb as r
from models.card import Card


@xfail
def test_entity_id(app, db_conn, cards_table):
    """
    Expect a card to require an entity_id.
    """
    assert False


@xfail
def test_previous_version_id(app, db_conn, cards_table):
    """
    Expect a card to allow a previous version id.
    """
    assert False


@xfail
def test_language(app, db_conn, cards_table):
    """
    Expect a card to require a language.
    """
    assert False


@xfail
def test_unit_id(app, db_conn, cards_table):
    """
    Expect a card to require a unit id.
    """
    assert False


@xfail
def test_name(app, db_conn, cards_table):
    """
    Expect a card to require a name.
    """
    assert False


@xfail
def test_canonical(app, db_conn, cards_table):
    """
    Expect a card version canoncial to be a boolean.
    """
    assert False


@xfail
def test_tags(app, db_conn, cards_table):
    """
    Expect a card to allow tags.
    """
    assert False


@xfail
def test_kind(app, db_conn, cards_table):
    """
    Expect a card to have a kind.
    """
    assert False
