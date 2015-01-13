import pytest

xfail = pytest.mark.xfail


@xfail
def test_created(app, db_conn, responses_table):
    """
    Expect to have a created date.
    """

    return False


@xfail
def test_user(app, db_conn, responses_table):
    """
    Expect to require a user ID.
    """

    return False


@xfail
def test_card(app, db_conn, responses_table):
    """
    Expect to require a card ID.
    """

    return False


@xfail
def test_unit(app, db_conn, responses_table):
    """
    Expect to require a unit ID.
    """

    return False


@xfail
def test_score(app, db_conn, responses_table):
    """
    Expect to have a score between 0 and 1 (including).
    """

    return False
