from models.vote import Vote


def test_user(app, db_conn, posts_table):
    """
    Expect a vote to require a user id.
    """

    vote, errors = Vote.insert({
        'topic_id': 'B',
        'replies_to_id': 'D',
        'response': True,
    })
    assert len(errors) == 1
    vote['user_id'] = 'A'
    vote, errors = vote.save()
    assert len(errors) == 0


def test_topic(app, db_conn, posts_table):
    """
    Expect a vote to require a topic id.
    """

    vote, errors = Vote.insert({
        'user_id': 'A',
        'replies_to_id': 'D',
        'response': True,
    })
    assert len(errors) == 1
    vote['topic_id'] = 'B'
    vote, errors = vote.save()
    assert len(errors) == 0


def test_body(app, db_conn, posts_table):
    """
    Expect a vote to allow, but not require, a body.
    """

    vote, errors = Vote.insert({
        'user_id': 'A',
        'topic_id': 'B',
        'replies_to_id': 'D',
        'response': True,
    })
    assert len(errors) == 0
    vote['body'] = 'A'
    vote, errors = vote.save()
    assert len(errors) == 0


def test_kind(app, db_conn, posts_table):
    """
    Expect a vote to always have a kind of vote.
    """

    vote = Vote({
        'user_id': 'A',
        'topic_id': 'B',
        'replies_to_id': 'D',
        'response': True,
    })
    del vote['kind']
    vote, errors = vote.save()
    assert len(errors) == 1
    vote['kind'] = 'vote'
    vote, errors = vote.save()
    assert len(errors) == 0


def test_replies(app, db_conn, posts_table):
    """
    Expect a vote to require a replies to id.
    """

    vote, errors = Vote.insert({
        'user_id': 'A',
        'topic_id': 'B',
        'response': True,
    })
    assert len(errors) == 1
    vote['replies_to_id'] = 'D'
    vote, errors = vote.save()
    assert len(errors) == 0


def test_response(app, db_conn, posts_table):
    """
    Expect a vote to require a response (None is okay).
    """

    vote = Vote({
        'user_id': 'A',
        'topic_id': 'B',
        'replies_to_id': 'D',
    })
    del vote['response']
    vote, errors = vote.save()
    assert len(errors) == 0
    vote['response'] = True
    vote, errors = vote.save()
    assert len(errors) == 0
