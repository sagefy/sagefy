from models.post import Post


def test_user(db_conn, posts_table):
    """
    Expect a post to require a user id.
    """

    post, errors = Post.insert(db_conn, {
        'topic_id': 'B',
        'body': 'C',
    })
    assert len(errors) == 1
    post['user_id'] = 'A'
    post, errors = post.save(db_conn)
    assert len(errors) == 0


def test_topic(db_conn, posts_table):
    """
    Expect a post to require a topic id.
    """

    post, errors = Post.insert(db_conn, {
        'user_id': 'A',
        'body': 'C',
    })
    assert len(errors) == 1
    post['topic_id'] = 'B'
    post, errors = post.save(db_conn)
    assert len(errors) == 0


def test_body(db_conn, posts_table):
    """
    Expect a post to require a body.
    """

    post, errors = Post.insert(db_conn, {
        'user_id': 'A',
        'topic_id': 'B',
    })
    assert len(errors) == 1
    post['body'] = 'C'
    post, errors = post.save(db_conn)
    assert len(errors) == 0


def test_kind(db_conn, posts_table):
    """
    Expect a post to have a kind.
    """

    post = Post({
        'user_id': 'A',
        'topic_id': 'B',
        'body': 'C',
    })
    del post['kind']
    post, errors = post.save(db_conn)
    assert len(errors) == 1
    post['kind'] = 'post'
    post, errors = post.save(db_conn)
    assert len(errors) == 0


def test_replies(db_conn, posts_table):
    """
    Expect a post to allow a replies to id.
    """

    prev, errors = Post.insert(db_conn, {
        'id': 'D',
        'user_id': 'A',
        'topic_id': 'B',
        'body': 'C',
    })
    post, errors = Post.insert(db_conn, {
        'user_id': 'A',
        'topic_id': 'B',
        'body': 'C',
    })
    assert len(errors) == 0
    post['replies_to_id'] = prev['id']
    post, errors = post.save(db_conn)
    assert len(errors) == 0
