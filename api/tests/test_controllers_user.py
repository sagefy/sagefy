import pytest


@pytest.mark.xfail
def test_user_get(app, db_conn):
    """
    Ensure a user can be retrieved by ID.
    """
    assert False


@pytest.mark.xfail
def test_user_get_failed(app, db_conn):
    """
    Ensure a no user is returned when ID doesn't match.
    """
    assert False


@pytest.mark.xfail
def test_user_get_current(app, db_conn):
    """
    Ensure the current user can be retrieved.
    """
    assert False


@pytest.mark.xfail
def test_user_get_current_failed(app, db_conn):
    """
    Ensure no user is returned when logged out.
    """
    assert False


@pytest.mark.xfail
def test_user_create(app, db_conn):
    """
    Ensure a user can be created.
    """
    assert False


@pytest.mark.xfail
def test_user_create_failed(app, db_conn):
    """
    Ensure a user will fail to create when invalid.
    """
    assert False


@pytest.mark.xfail
def test_user_login(app, db_conn):
    """
    Ensure a user can login.
    """
    assert False


@pytest.mark.xfail
def test_user_login_none(app, db_conn):
    """
    Ensure a user can't login if no user by name.
    """
    assert False


@pytest.mark.xfail
def test_user_login_password_fail(app, db_conn):
    """
    Ensure a user can't login if password is wrong.
    """
    assert False


@pytest.mark.xfail
def test_user_logout(app, db_conn):
    """
    Ensure a user can log out.
    """
    assert False


@pytest.mark.xfail
def test_user_update(app, db_conn):
    """
    Ensure a user can be updated.
    """
    assert False


@pytest.mark.xfail
def test_user_update_none(app, db_conn):
    """
    Ensure a user won't update if not exist.
    """
    assert False


@pytest.mark.xfail
def test_user_update_self_only(app, db_conn):
    """
    Ensure a user can only update herself.
    """
    assert False


@pytest.mark.xfail
def test_user_update_invalid(app, db_conn):
    """
    Ensure a user won't update if invalid.
    """
    assert False
