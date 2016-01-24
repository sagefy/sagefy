from models.vote import Vote


def create_proposal(posts_table, units_table, db_conn):
    posts_table.insert({
        'id': 'D',
        'user_id': 'C',
        'topic_id': 'B',
        'body': '_',
        'kind': 'proposal',
        'entity_version': {
            'id': 'E',
            'kind': 'unit',
        },
        'name': 'make unit'
    }).run(db_conn)

    units_table.insert({
        'id': 'E',
        'entity_id': 'F',
        'status': 'pending',
    }).run(db_conn)


def test_user(db_conn, posts_table, units_table):
    """
    Expect a vote to require a user id.
    """

    create_proposal(posts_table, units_table, db_conn)
    vote, errors = Vote.insert(db_conn, {
        'topic_id': 'B',
        'replies_to_id': 'D',
        'response': True,
    })
    assert len(errors) == 1
    vote['user_id'] = 'A'
    vote, errors = vote.save(db_conn)
    assert len(errors) == 0


def test_topic(db_conn, posts_table, units_table):
    """
    Expect a vote to require a topic id.
    """

    create_proposal(posts_table, units_table, db_conn)
    vote, errors = Vote.insert(db_conn, {
        'user_id': 'A',
        'replies_to_id': 'D',
        'response': True,
    })
    assert len(errors) == 1
    vote['topic_id'] = 'B'
    vote, errors = vote.save(db_conn)
    assert len(errors) == 0


def test_body(db_conn, posts_table, units_table):
    """
    Expect a vote to allow, but not require, a body.
    """

    create_proposal(posts_table, units_table, db_conn)
    vote, errors = Vote.insert(db_conn, {
        'user_id': 'A',
        'topic_id': 'B',
        'replies_to_id': 'D',
        'response': True,
    })
    assert len(errors) == 0
    vote['body'] = 'A'
    vote, errors = vote.save(db_conn)
    assert len(errors) == 0


def test_kind(db_conn, posts_table, units_table):
    """
    Expect a vote to always have a kind of vote.
    """

    create_proposal(posts_table, units_table, db_conn)
    vote = Vote({
        'user_id': 'A',
        'topic_id': 'B',
        'replies_to_id': 'D',
        'response': True,
    })
    del vote['kind']
    vote, errors = vote.save(db_conn)
    assert len(errors) == 1
    vote['kind'] = 'vote'
    vote, errors = vote.save(db_conn)
    assert len(errors) == 0


def test_replies(db_conn, posts_table, units_table):
    """
    Expect a vote to require a replies to id.
    """

    create_proposal(posts_table, units_table, db_conn)
    vote, errors = Vote.insert(db_conn, {
        'user_id': 'A',
        'topic_id': 'B',
        'response': True,
    })
    assert len(errors) == 1
    vote['replies_to_id'] = 'D'
    vote, errors = vote.save(db_conn)
    assert len(errors) == 0


def test_response(db_conn, posts_table, units_table):
    """
    Expect a vote to require a response.
    """

    create_proposal(posts_table, units_table, db_conn)
    vote = Vote({
        'user_id': 'A',
        'topic_id': 'B',
        'replies_to_id': 'D',
    })
    del vote['response']
    vote, errors = vote.save(db_conn)
    assert len(errors) == 0
    vote['response'] = True
    vote, errors = vote.save(db_conn)
    assert len(errors) == 0
