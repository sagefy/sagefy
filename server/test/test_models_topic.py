from models.topic import Topic


def test_user_id(db_conn, topics_table):
    """
    Expect a topic to require a user id.
    """

    topic, errors = Topic.insert(db_conn, {
        'name': 'A',
        'entity': {
            'id': 'A',
            'kind': 'card',
        }
    })
    assert len(errors) == 1
    topic['user_id'] = 'Q'
    topic, errors = topic.save(db_conn)
    assert len(errors) == 0


def test_name(db_conn, topics_table):
    """
    Expect a topic to require a name.
    """

    topic, errors = Topic.insert(db_conn, {
        'user_id': 'Q',
        'entity': {
            'id': 'A',
            'kind': 'card',
        }
    })
    assert len(errors) == 1
    topic['name'] = 'A'
    topic, errors = topic.save(db_conn)
    assert len(errors) == 0


def test_entity(db_conn, topics_table):
    """
    Expect a topic to require an entity kind and id.
    """

    topic, errors = Topic.insert(db_conn, {
        'user_id': 'Q',
        'name': 'A',
    })
    assert len(errors) == 2
    topic['entity'] = {
        'id': 'A',
        'kind': 'card',
    }
    topic, errors = topic.save(db_conn)
    assert len(errors) == 0


def test_list_by_entity_id(db_conn, topics_table):
    topics_table.insert([{
        'user_id': 'Q',
        'name': 'A',
        'entity': {
            'id': 'A',
            'kind': 'card',
        }
    }, {
        'user_id': 'Q',
        'name': 'A',
        'entity': {
            'id': 'A',
            'kind': 'card',
        }
    }, {
        'user_id': 'Q',
        'name': 'A',
        'entity': {
            'id': 'B',
            'kind': 'card',
        }
    }]).run(db_conn)

    topics = Topic.list_by_entity_id(db_conn, 'A')
    assert len(topics) == 2
