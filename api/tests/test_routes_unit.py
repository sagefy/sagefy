import pytest

xfail = pytest.mark.xfail


@xfail
def test_get_unit(app, db_conn,
                  units_table, sets_table, topics_table):
    """
    Expect to get the unit information for displaying to a contributor.
    """

    assert False

    # TODO provide model data
    # TODO join through requires
    # TODO join through sets
    # TODO list of topics
    # TODO list of versions
    # TODO sequencer data: learners, quality, difficulty


def test_get_unit_404(app, db_conn):
    """
    Expect to fail to get an unknown unit (404).
    """

    response = app.test_client().get('/api/units/abcd/')
    assert response.status_code == 404
