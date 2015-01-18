from models.post import Post


def test_user(app, db_conn, posts_table):
    """
    Expect a post to require a user id.
    """

    post, errors = Post.insert({
        'topic_id': 'B',
        'body': 'C',
    })
    assert len(errors) == 1
    post['user_id'] = 'A'
    post, errors = post.save()
    assert len(errors) == 0


def test_topic(app, db_conn, posts_table):
    """
    Expect a post to require a topic id.
    """

    post, errors = Post.insert({
        'user_id': 'A',
        'body': 'C',
    })
    assert len(errors) == 1
    post['topic_id'] = 'B'
    post, errors = post.save()
    assert len(errors) == 0


def test_body(app, db_conn, posts_table):
    """
    Expect a post to require a body.
    """

    post, errors = Post.insert({
        'user_id': 'A',
        'topic_id': 'B',
    })
    assert len(errors) == 1
    post['body'] = 'C'
    post, errors = post.save()
    assert len(errors) == 0


def test_kind(app, db_conn, posts_table):
    """
    Expect a post to have a kind.
    """

    post = Post({
        'user_id': 'A',
        'topic_id': 'B',
        'body': 'C',
    })
    del post['kind']
    post, errors = post.save()
    assert len(errors) == 1
    post['kind'] = 'post'
    post, errors = post.save()
    assert len(errors) == 0


def test_replies(app, db_conn, posts_table):
    """
    Expect a post to allow a replies to id.
    """

    post, errors = Post.insert({
        'user_id': 'A',
        'topic_id': 'B',
        'body': 'C',
    })
    assert len(errors) == 0
    post['replies_to_id'] = 'D'
    post, errors = post.save()
    assert len(errors) == 0
