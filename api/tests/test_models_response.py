import pytest

xfail = pytest.mark.xfail


@xfail
def test_created(app, db_conn, responses_table):
    """
    Expect to have a created date.
    """

    assert False


@xfail
def test_user(app, db_conn, responses_table):
    """
    Expect to require a user ID.
    """

    assert False


@xfail
def test_card(app, db_conn, responses_table):
    """
    Expect to require a card ID.
    """

    assert False


@xfail
def test_unit(app, db_conn, responses_table):
    """
    Expect to require a unit ID.
    """

    assert False


@xfail
def test_score(app, db_conn, responses_table):
    """
    Expect to have a score between 0 and 1 (including).
    """

    assert False
