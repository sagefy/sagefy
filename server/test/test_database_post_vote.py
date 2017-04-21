from database.post import insert_post


def create_proposal(posts_table, units_table, db_conn):
    posts_table.insert({
        'id': 'D',
        'user_id': 'C',
        'topic_id': 'B',
        'body': '_',
        'kind': 'proposal',
        'entity_versions': [{
            'id': 'E',
            'kind': 'unit',
        }],
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
    vote, errors = insert_post({
        'kind': 'vote',
        'topic_id': 'B',
        'replies_to_id': 'D',
        'response': True,
    }, db_conn)
    assert len(errors) == 1
    vote['user_id'] = 'A'
    vote, errors = insert_post(vote, db_conn)
    assert len(errors) == 0


def test_topic(db_conn, posts_table, units_table):
    """
    Expect a vote to require a topic id.
    """

    create_proposal(posts_table, units_table, db_conn)
    vote, errors = insert_post({
        'kind': 'vote',
        'user_id': 'A',
        'replies_to_id': 'D',
        'response': True,
    }, db_conn)
    assert len(errors) == 1
    vote['topic_id'] = 'B'
    vote, errors = insert_post(vote, db_conn)
    assert len(errors) == 0


def test_body(db_conn, posts_table, units_table):
    """
    Expect a vote to allow, but not require, a body.
    """

    create_proposal(posts_table, units_table, db_conn)
    vote, errors = insert_post({
        'kind': 'vote',
        'user_id': 'A',
        'topic_id': 'B',
        'replies_to_id': 'D',
        'response': True,
    }, db_conn)
    assert len(errors) == 0
    vote['body'] = 'A'
    vote['user_id'] = 'B'
    vote, errors = insert_post(vote, db_conn)
    assert len(errors) == 0


def test_replies(db_conn, posts_table, units_table):
    """
    Expect a vote to require a replies to id.
    """

    create_proposal(posts_table, units_table, db_conn)
    vote, errors = insert_post({
        'kind': 'vote',
        'user_id': 'A',
        'topic_id': 'B',
        'response': True,
    }, db_conn)
    assert len(errors) == 1
    vote['replies_to_id'] = 'D'
    vote, errors = insert_post(vote, db_conn)
    assert len(errors) == 0


def test_response(db_conn, posts_table, units_table):
    """
    Expect a vote to require a response.
    """

    create_proposal(posts_table, units_table, db_conn)
    vote, errors = insert_post({
        'kind': 'vote',
        'user_id': 'A',
        'topic_id': 'B',
        'replies_to_id': 'D',
    }, db_conn)
    assert len(errors) == 1
    vote['response'] = True
    vote, errors = insert_post(vote, db_conn)
    assert len(errors) == 0
