import pytest

xfail = pytest.mark.xfail


@xfail
def test_search(app, db_conn):
    """
    Expect to search by query.
    """
    return False


@xfail
def test_search_topics(app, db_conn):
    """
    Expect to search only topics.
    """
    return False


@xfail
def test_search_language(app, db_conn, users_table, topics_table,
                         posts_table):
    """
    Expect to search by language.
    """
    return False


@xfail
def test_search_topics_user(app, db_conn, users_table, topics_table,
                            posts_table):
    """
    Expect to search topics by user.
    """
    return False


@xfail
def test_search_topics_versions(app, db_conn, users_table, topics_table,
                                posts_table):
    """
    Expect to search for versions.
    """
    return False


@xfail
def test_search_sort(app, db_conn, users_table, topics_table,
                     posts_table):
    """
    Expect to sort in search.
    """
    return False


@xfail
def test_search_paginate(app, db_conn, users_table, topics_table,
                         posts_table):
    """
    Expect to paginate in search.
    """
    return False


@xfail
def test_search_blank(app, db_conn, users_table, topics_table,
                      posts_table):
    """
    Expect a blank search result.
    """
    return False
