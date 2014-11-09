import pytest

xfail = pytest.mark.xfail


@xfail
def test_search(app, db_conn):
    """
    Expect to search topics by query.
    """
    return False


@xfail
def test_search_filter(app, db_conn):
    """
    Expect to search topics by kind.
    """
    return False


@xfail
def test_search_lang(app, db_conn):
    """
    Expect to search topics by language.
    """
    return False


@xfail
def test_search_user(app, db_conn):
    """
    Expect to search topics by user.
    """
    return False


@xfail
def test_search_proposal(app, db_conn):
    """
    Expect to search for proposals
    """
    return False


@xfail
def test_search_sort(app, db_conn):
    """
    Expect to sort topics in search.
    """
    return False


@xfail
def test_search_paginate(app, db_conn):
    """
    Expect to paginate topics in search.
    """
    return False


@xfail
def test_search_blank(app, db_conn):
    """
    Expect a blank search result.
    """
    return False


@xfail
def test_create_topic(app, db_conn):
    """
    Expect to create a topic with post.
    """
    return False


@xfail
def test_create_topic_proposal(app, db_conn):
    """
    Expect to create a topic with proposal.
    """
    return False


@xfail
def test_create_topic_flag(app, db_conn):
    """
    Expect to create topic with a flag.
    """
    return False


@xfail
def test_create_topic_login(app, db_conn):
    """
    Expect create topic to fail when logged out.
    """
    return False


@xfail
def test_create_topic_no_post(app, db_conn):
    """
    Expect create topic to fail without post.
    """
    return False


@xfail
def test_topic_update(app, db_conn):
    """
    Expect to update topic name.
    """
    return False


@xfail
def test_update_topic_author(app, db_conn):
    """
    Expect update topic to require original author.
    """
    return False


@xfail
def test_update_topic_fields(app, db_conn):
    """
    Expect update topic to only change name.
    """
    return False


@xfail
def test_get_posts(app, db_conn):
    """
    Expect to get posts for given topic.
    """
    return False


@xfail
def test_get_posts_not_topic(app, db_conn):
    """
    Expect 404 to get posts for a nonexistant topic.
    """
    return False


@xfail
def test_get_posts_paginate(app, db_conn):
    """
    Expect get posts for topic to paginate.
    """
    return False


@xfail
def test_get_posts_proposal(app, db_conn):
    """
    Expect get posts for topic to render a proposal correctly.
    """
    return False


@xfail
def test_get_posts_votes(app, db_conn):
    """
    Expect get posts for topic to render votes correctly.
    """
    return False


@xfail
def test_create_post(app, db_conn):
    """
    Expect create post.
    """
    return False


@xfail
def test_create_post_errors(app, db_conn):
    """
    Expect create post missing field to show errors.
    """
    return False


@xfail
def test_create_post_login(app, db_conn):
    """
    Expect create post to require login.
    """
    return False


@xfail
def test_create_post_proposal(app, db_conn):
    """
    Expect create post to create a proposal.
    """
    return False


@xfail
def test_create_post_vote(app, db_conn):
    """
    Expect create post to create a vote.
    """
    return False


@xfail
def test_update_post_login(app, db_conn):
    """
    Expect update post to require login.
    """
    return False


@xfail
def test_update_post_author(app, db_conn):
    """
    Expect update post to require own post.
    """
    return False


@xfail
def test_update_post_body(app, db_conn):
    """
    Expect update post to change body only for general post.
    """
    return False


@xfail
def test_update_proposal(app, db_conn):
    """
    Expect update post to handle proposals correctly.
    """
    return False
