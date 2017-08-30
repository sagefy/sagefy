from database.topic import insert_topic, list_topics_by_entity_id


def test_user_id(db_conn, topics_table):
    """
    Expect a topic to require a user id.
    """

    topic_data = {
        'name': 'A',
        'entity': {
            'id': 'A',
            'kind': 'card',
        }
    }
    topic, errors = insert_topic(db_conn, topic_data)
    assert len(errors) == 1
    topic_data['user_id'] = 'Q'
    topic, errors = insert_topic(db_conn, topic_data)
    assert len(errors) == 0


def test_name(db_conn, topics_table):
    """
    Expect a topic to require a name.
    """

    topic_data = {
        'user_id': 'Q',
        'entity': {
            'id': 'A',
            'kind': 'card',
        }
    }
    topic, errors = insert_topic(db_conn, topic_data)
    assert len(errors) == 1
    topic_data['name'] = 'A'
    topic, errors = insert_topic(db_conn, topic_data)
    assert len(errors) == 0


def test_entity(db_conn, topics_table):
    """
    Expect a topic to require an entity kind and id.
    """

    topic_data = {
        'user_id': 'Q',
        'name': 'A',
    }
    topic, errors = insert_topic(db_conn, topic_data)
    assert len(errors) == 2
    topic_data['entity'] = {
        'id': 'A',
        'kind': 'card',
    }
    topic, errors = insert_topic(db_conn, topic_data)
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

    topics = list_topics_by_entity_id(db_conn, 'A', {})
    assert len(topics) == 2
