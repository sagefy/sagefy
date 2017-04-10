from database.post import insert_post


def test_user_id(db_conn, posts_table):
    """
    Expect a proposal to require a user id.
    """

    proposal, errors = insert_post({
        'kind': 'proposal',
        'topic_id': 'B',
        'body': 'C',
        'entity_version': {
            'id': 'D',
            'kind': 'unit'
        },
        'name': 'E',
    }, db_conn)
    assert len(errors) == 1
    proposal['user_id'] = 'A'
    proposal, errors = insert_post(proposal, db_conn)
    assert len(errors) == 0


def test_topic(db_conn, posts_table):
    """
    Expect a proposal to require a topic id.
    """

    proposal, errors = insert_post({
        'kind': 'proposal',
        'user_id': 'A',
        'body': 'C',
        'entity_version': {
            'id': 'D',
            'kind': 'unit'
        },
        'name': 'E',
    }, db_conn)
    assert len(errors) == 1
    proposal['topic_id'] = 'B'
    proposal, errors = insert_post(proposal, db_conn)
    assert len(errors) == 0


def test_body(db_conn, posts_table):
    """
    Expect a proposal to require a body.
    """

    proposal, errors = insert_post({
        'kind': 'proposal',
        'user_id': 'A',
        'topic_id': 'B',
        'entity_version': {
            'id': 'D',
            'kind': 'unit'
        },
        'name': 'E',
    }, db_conn)
    assert len(errors) == 1
    proposal['body'] = 'C'
    proposal, errors = insert_post(proposal, db_conn)
    assert len(errors) == 0


def test_replies(db_conn, posts_table):
    """
    Expect a proposal to allow a replies to id.
    """

    prev, errors = insert_post({
        'kind': 'post',
        'user_id': 'A',
        'topic_id': 'B',
        'body': 'C',
    }, db_conn)
    proposal, errors = insert_post({
        'kind': 'proposal',
        'user_id': 'A',
        'topic_id': 'B',
        'body': 'C',
        'entity_version': {
            'id': 'D',
            'kind': 'unit'
        },
        'name': 'E',
        'replies_to_id': prev['id'],
    }, db_conn)
    assert len(errors) == 0


def test_entity(db_conn, posts_table):
    """
    Expect a proposal to require an entity version id.
    """

    proposal, errors = insert_post({
        'kind': 'proposal',
        'user_id': 'A',
        'topic_id': 'B',
        'body': 'C',
        'name': 'E',
    }, db_conn)
    assert len(errors) == 2
    proposal['entity_version'] = {
        'id': 'D',
        'kind': 'unit'
    }
    proposal, errors = insert_post(proposal, db_conn)
    assert len(errors) == 0


def test_name(db_conn, posts_table):
    """
    Expect a proposal to require a name.
    """

    proposal, errors = insert_post({
        'kind': 'proposal',
        'user_id': 'A',
        'topic_id': 'B',
        'body': 'C',
        'entity_version': {
            'id': 'D',
            'kind': 'unit'
        }
    }, db_conn)
    assert len(errors) == 1
    proposal['name'] = 'E'
    proposal, errors = insert_post(proposal, db_conn)
    assert len(errors) == 0
