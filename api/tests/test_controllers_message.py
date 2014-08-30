import pytest
import rethinkdb as r


@pytest.mark.xfail
def test_a(app, db_conn, messages_table):
    """
    Expect to require login to list messages.
    """
    assert False


@pytest.mark.xfail
def test_b(app, db_conn, messages_table):
    """
    Expect to require user to be member to list messages.
    """
    assert False


@pytest.mark.xfail
def test_c(app, db_conn, messages_table):
    """
    Expect to list messages.
    """
    assert False


@pytest.mark.xfail
def test_d(app, db_conn, messages_table):
    """
    Expect to paginate listed messages.
    """
    assert False


@pytest.mark.xfail
def test_e(app, db_conn, messages_table):
    """
    Expect to require login to get a message.
    """
    assert False


@pytest.mark.xfail
def test_f(app, db_conn, messages_table):
    """
    Expect to 404 if no matching message.
    """
    assert False


@pytest.mark.xfail
def test_g(app, db_conn, messages_table):
    """
    Expect to require user to be member to get message.
    """
    assert False


@pytest.mark.xfail
def test_h(app, db_conn, messages_table):
    """
    Expect to get a message.
    """
    assert False


@pytest.mark.xfail
def test_i(app, db_conn, messages_table):
    """
    Expect to require login to mark message as read.
    """
    assert False


@pytest.mark.xfail
def test_j(app, db_conn, messages_table):
    """
    Expect to 404 if no matching message when marking as read.
    """
    assert False


@pytest.mark.xfail
def test_k(app, db_conn, messages_table):
    """
    Expect to require own message to mark as read.
    """
    assert False


@pytest.mark.xfail
def test_l(app, db_conn, messages_table):
    """
    Expect to mark a message as read.
    """
    assert False


@pytest.mark.xfail
def test_m(app, db_conn, messages_table):
    """
    Expect to require login to create a message.
    """
    assert False


@pytest.mark.xfail
def test_n(app, db_conn, messages_table):
    """
    Expect to insert a message with the correct from user.
    """
    assert False


@pytest.mark.xfail
def test_o(app, db_conn, messages_table):
    """
    Expect to show errors if error when insert message.
    """
    assert False


@pytest.mark.xfail
def test_p(app, db_conn, messages_table):
    """
    Expect to create a message.
    """
    assert False
