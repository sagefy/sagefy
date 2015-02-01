from modules.validations import is_required, is_email, has_min_length
import pytest

xfail = pytest.mark.xfail


def test_require(app, db_conn):
    """
    Expect a validation to require a field.
    """
    assert is_required('test') is None
    assert is_required(None)


def test_email(app, db_conn):
    """
    Expect a validation to validate email format.
    """
    assert is_email('test@example.com') is None
    assert is_email('other')


def test_minlength(app, db_conn):
    """
    Expect a validation to require a minimum length.
    """
    assert has_min_length('abcd1234', 8) is None
    assert has_min_length('a', 8)


@xfail
def test_boolean(app, db_conn):
    """
    Expect
    """
    assert False


@xfail
def test_string(app, db_conn):
    """
    Expect
    """
    assert False


@xfail
def test_number(app, db_conn):
    """
    Expect
    """
    assert False


@xfail
def test_language(app, db_conn):
    """
    Expect
    """
    assert False


@xfail
def test_list(app, db_conn):
    """
    Expect
    """
    assert False


@xfail
def test_one_of(app, db_conn):
    """
    Expect
    """
    assert False


@xfail
def test_entity(app, db_conn):
    """
    Expect
    """
    assert False


@xfail
def test_list_entity(app, db_conn):
    """
    Expect
    """
    assert False


@xfail
def test_list_string(app, db_conn):
    """
    Expect
    """
    assert False
