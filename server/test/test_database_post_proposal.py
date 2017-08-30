from database.post import insert_post


def create_unit_ad(db_conn, units_table):
    """
    Create a unit for the following tests.
    """

    units_table.insert({
        'user_id': 'abcd1234',
        'entity_id': 'A',
        'id': 'D',
        'status': 'accepted',
    }).run(db_conn)


def test_user_id(db_conn, posts_table, units_table):
    """
    Expect a proposal to require a user id.
    """

    create_unit_ad(db_conn, units_table)
    proposal, errors = insert_post({
        'kind': 'proposal',
        'topic_id': 'B',
        'body': 'C',
        'entity_versions': [{
            'id': 'D',
            'kind': 'unit'
        }],
    }, db_conn)
    assert len(errors) == 1
    proposal['user_id'] = 'A'
    proposal, errors = insert_post(db_conn, proposal)
    assert len(errors) == 0


def test_topic(db_conn, posts_table, units_table):
    """
    Expect a proposal to require a topic id.
    """

    create_unit_ad(db_conn, units_table)
    proposal, errors = insert_post({
        'kind': 'proposal',
        'user_id': 'A',
        'body': 'C',
        'entity_versions': [{
            'id': 'D',
            'kind': 'unit'
        }],
    }, db_conn)
    assert len(errors) == 1
    proposal['topic_id'] = 'B'
    proposal, errors = insert_post(db_conn, proposal)
    assert len(errors) == 0


def test_body(db_conn, posts_table, units_table):
    """
    Expect a proposal to require a body.
    """

    create_unit_ad(db_conn, units_table)
    proposal, errors = insert_post({
        'kind': 'proposal',
        'user_id': 'A',
        'topic_id': 'B',
        'entity_versions': [{
            'id': 'D',
            'kind': 'unit'
        }],
    }, db_conn)
    assert len(errors) == 1
    proposal['body'] = 'C'
    proposal, errors = insert_post(db_conn, proposal)
    assert len(errors) == 0


def test_replies(db_conn, posts_table, units_table):
    """
    Expect a proposal to allow a replies to id.
    """

    create_unit_ad(db_conn, units_table)
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
        'entity_versions': [{
            'id': 'D',
            'kind': 'unit'
        }],
        'replies_to_id': prev['id'],
    }, db_conn)
    assert len(errors) == 0


def test_entity(db_conn, posts_table, units_table):
    """
    Expect a proposal to require an entity version id.
    """

    create_unit_ad(db_conn, units_table)
    proposal, errors = insert_post({
        'kind': 'proposal',
        'user_id': 'A',
        'topic_id': 'B',
        'body': 'C',
    }, db_conn)
    assert len(errors) == 1
    proposal['entity_versions'] = [{
        'id': 'D',
        'kind': 'unit'
    }]
    proposal, errors = insert_post(db_conn, proposal)
    assert len(errors) == 0
