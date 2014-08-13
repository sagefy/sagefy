from models.user import User
import pytest


@pytest.mark.xfail
def test_user_name_required(app, db_conn):
    """
    Ensure a name is required.
    """
    assert False


@pytest.mark.xfail
def test_user_name_unique(app, db_conn):
    """
    Ensure a name is unique.
    """
    assert False


@pytest.mark.xfail
def test_user_email_required(app, db_conn):
    """
    Ensure an email is required.
    """
    assert False


@pytest.mark.xfail
def test_user_email_unique(app, db_conn):
    """
    Ensure an email is unique.
    """
    assert False


@pytest.mark.xfail
def test_user_email_format(app, db_conn):
    """
    Ensure an email is formatted.
    """
    assert False


@pytest.mark.xfail
def test_user_password_required(app, db_conn):
    """
    Ensure a password is required.
    """
    assert False


@pytest.mark.xfail
def test_user_password_minlength(app, db_conn):
    """
    Ensure an password is long enough.
    """
    assert False


@pytest.mark.xfail
def test_user_no_password(app, db_conn):
    """
    Ensure an password isn't provided if not current user.
    """
    assert False


@pytest.mark.xfail
def test_user_email_current(app, db_conn):
    """
    Ensure an email is only provided when current user.
    """
    assert False


@pytest.mark.xfail
def test_user_password_encrypt(app, db_conn):
    """
    Ensure a password is encrypted before going into db.
    """
    assert False


@pytest.mark.xfail
def test_user_password_validate(app, db_conn):
    """
    Ensure a password can be validated.
    """
    assert False


@pytest.mark.xfail
def test_user_current(app, db_conn):
    """
    Ensure a user can be tested if she is the current user.
    """
    assert False
