from models.follow2 import Follow


def test_user_id(app, db_conn, follows_table):
    """
    A follow should require a user_id.
    """

    follow, errors = Follow.insert({
        'entity': {
            'id': 'A',
            'kind': 'card',
        }
    })
    assert len(errors) == 1
    follow['user_id'] = 'A'
    follow, errors = follow.save()
    assert len(errors) == 0


def test_entity(app, db_conn, follows_table):
    """
    Expect a follow to require an entity kind and id.
    """

    follow, errors = Follow.insert({
        'user_id': 'A',
    })
    assert len(errors) == 1
    follow['entity'] = {
        'id': 'A',
        'kind': 'card',
    }
    follow, errors = follow.save()
    assert len(errors) == 0
