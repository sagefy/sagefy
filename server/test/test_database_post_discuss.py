from database.post import list_posts


def test_list_posts_facade(db_conn, posts_table):
    """
    Expect to get a list of posts, and the instances to match the kinds.
    """

    posts_data = [{
        'id': 'fghj4567',
        'user_id': 'abcd1234',
        'topic_id': 'wxyz7890',
        'body': 'abcd',
        'kind': 'post',
    }, {
        'id': 'yuio6789',
        'user_id': 'abcd1234',
        'topic_id': 'wxyz7890',
        'kind': 'vote',
        'replies_to_id': 'fghj4567',
    }, {
        'id': 'bnml3456',
        'user_id': 'abcd1234',
        'topic_id': 'erty4567',
        'body': 'abcd',
        'kind': 'post',
    }]
    posts_table.insert(posts_data).run(db_conn)
    posts = list_posts({'topic_id': 'wxyz7890'}, db_conn)
    assert len(posts) == 2
    assert posts[0]['id'] in ('fghj4567', 'yuio6789')
    assert posts[1]['id'] in ('fghj4567', 'yuio6789')
