import pytest

xfail = pytest.mark.xfail


@xfail
def test_get_set(app, db_conn,
                 sets_table, units_table, topics_table):
    """
    Expect to get the set information for displaying to a contributor.
    """

    assert False

    # TODO@ model data
    # TODO@ join through units
    # TODO@ list of topics
    # TODO@ list of versions
    # TODO@ sequencer: learners, quality, difficulty


def test_get_set_404(app, db_conn):
    """
    Expect to fail to get set information if set is unknown. (404)
    """

    response = app.test_client().get('/api/sets/abcd/')
    assert response.status_code == 404


@xfail
def test_set_tree():
    """
    Expect to get set information in tree format.
    """

    assert False


@xfail
def test_set_tree_401():
    """
    Expect to fail to get set in tree format if not log in. (401)
    """

    assert False


@xfail
def test_set_tree_404():
    """
    Expect to fail to get set in tree format if no set. (404)
    """

    assert False


@xfail
def test_set_tree_400():
    """
    Expect to fail to get set in tree format
    if parameters don't make sense. (400)
    """

    assert False


@xfail
def test_set_units():
    """
    Expect to provide list of units to choose from.
    """

    assert False


@xfail
def test_set_units_401():
    """
    Expect to fail to provide list of units if not log in. (401)
    """

    assert False


@xfail
def test_set_units_404():
    """
    Expect to fail to provide list of units if set not found. (404)
    """

    assert False


@xfail
def test_set_units_400():
    """
    Expect to fail to provide list of units if request is nonsense. (400)
    """

    assert False


@xfail
def test_choose_unit():
    """
    Expect to let a learner choose their unit.
    """

    assert False


@xfail
def test_choose_unit_401():
    """
    Expect to fail to choose unit if not log in. (401)
    """

    assert False


@xfail
def test_choose_unit_404():
    """
    Expect to fail to choose unit if unit doesn't exist. (404)
    """

    assert False


@xfail
def test_choose_unit_400():
    """
    Expect to fail to choose unit if request is nonsense. (400)
    """

    assert False
