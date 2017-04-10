from database.post import insert_post


def test_user(db_conn, posts_table):
    """
    Expect a post to require a user id.
    """

    post, errors = insert_post({
        'kind': 'post',
        'topic_id': 'B',
        'body': 'C',
    }, db_conn)
    assert len(errors) == 1
    post, errors = insert_post({
        'user_id': 'A',
        'kind': 'post',
        'topic_id': 'B',
        'body': 'C',
    }, db_conn)
    assert len(errors) == 0


def test_topic(db_conn, posts_table):
    """
    Expect a post to require a topic id.
    """

    post, errors = insert_post({
        'kind': 'post',
        'user_id': 'A',
        'body': 'C',
    }, db_conn)
    assert len(errors) == 1
    post, errors = insert_post({
        'kind': 'post',
        'user_id': 'A',
        'body': 'C',
        'topic_id': 'B',
    }, db_conn)
    assert len(errors) == 0


def test_body(db_conn, posts_table):
    """
    Expect a post to require a body.
    """

    post, errors = insert_post({
        'kind': 'post',
        'user_id': 'A',
        'topic_id': 'B',
    }, db_conn)
    assert len(errors) == 1
    post, errors = insert_post({
        'kind': 'post',
        'user_id': 'A',
        'topic_id': 'B',
        'body': 'C',
    }, db_conn)
    assert len(errors) == 0


def test_kind(db_conn, posts_table):
    """
    Expect a post to have a kind.
    """

    post, errors = insert_post({
        'user_id': 'A',
        'topic_id': 'B',
        # 'body': 'C',
    }, db_conn)
    assert len(errors) == 1
    post, errors = insert_post({
        'user_id': 'A',
        'topic_id': 'B',
        'body': 'C',
        'kind': 'post',
    }, db_conn)
    assert len(errors) == 0


def test_replies(db_conn, posts_table):
    """
    Expect a post to allow a replies to id.
    """

    prev, errors = insert_post({
        'id': 'D',
        'user_id': 'A',
        'topic_id': 'B',
        'body': 'C',
        'kind': 'post',
    }, db_conn)
    assert len(errors) == 0
    post, errors = insert_post({
        'user_id': 'A',
        'topic_id': 'B',
        'body': 'C',
        'kind': 'post',
        'replies_to_id': prev['id'],
    }, db_conn)
    assert len(errors) == 0
