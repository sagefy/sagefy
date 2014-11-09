import pytest
# import modules.discuss as discuss

xfail = pytest.mark.xfail


@xfail
def test_get_post_facade(app, db_conn):
    """
    Expect to get a post, and the instance to match the kind.
    """
    return False


@xfail
def test_get_posts_facade(app, db_conn):
    """
    Expect to get a list of posts, and the instances to match the kinds.
    """
    return False


@xfail
def create_post_facade(app, db_conn):
    """
    Expect to a create a post, and the right kind of instance.s
    """
    return False
