import pytest

xfail = pytest.mark.xfail


@xfail
def test_entity(app, db_conn, sets_table):
    """
    Expect a set to require an entity_id.
    """
    return False


@xfail
def test_previous(app, db_conn, sets_table):
    """
    Expect a set to allow a previous version id.
    """
    return False


@xfail
def test_language(app, db_conn, sets_table):
    """
    Expect a set to require a language.
    """
    return False


@xfail
def test_name(app, db_conn, sets_table):
    """
    Expect a set to require a name.
    """
    return False


@xfail
def test_body(app, db_conn, sets_table):
    """
    Expect a set to require a body.
    """
    return False


@xfail
def test_canonical(app, db_conn, sets_table):
    """
    Expect a set canonical to be a boolean.
    """
    return False


@xfail
def test_tags(app, db_conn, sets_table):
    """
    Expect a set to allow tags.
    """
    return False


@xfail
def test_members(app, db_conn, sets_table):
    """
    Expect a set to record a list of members.
    """
    return False
