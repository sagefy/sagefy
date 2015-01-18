import pytest

xfail = pytest.mark.xfail

from models.topic import Topic


def test_user_id(app, db_conn, topics_table):
    """
    Expect a topic to require a user id.
    """

    topic, errors = Topic.insert({
        'name': 'A',
        'entity': {
            'id': 'A',
            'kind': 'card',
        }
    })
    assert len(errors) == 1
    topic['user_id'] = 'Q'
    topic, errors = topic.save()
    assert len(errors) == 0


def test_name(app, db_conn, topics_table):
    """
    Expect a topic to require a name.
    """

    topic, errors = Topic.insert({
        'user_id': 'Q',
        'entity': {
            'id': 'A',
            'kind': 'card',
        }
    })
    assert len(errors) == 1
    topic['name'] = 'A'
    topic, errors = topic.save()
    assert len(errors) == 0


def test_entity(app, db_conn, topics_table):
    """
    Expect a topic to require an entity kind and id.
    """

    topic, errors = Topic.insert({
        'user_id': 'Q',
        'name': 'A',
    })
    assert len(errors) == 1
    topic['entity'] = {
        'id': 'A',
        'kind': 'card',
    }
    topic, errors = topic.save()
    assert len(errors) == 0
