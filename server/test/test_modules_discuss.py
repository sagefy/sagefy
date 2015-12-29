import modules.discuss as discuss
from models.post import Post
from models.proposal import Proposal
from models.vote import Vote


def test_instance(db_conn):
    """
    Expect to take post data, and from it produce a post instance per kind.
    """
    assert isinstance(discuss.instance({'kind': 'post'}), Post)
    assert isinstance(discuss.instance({'kind': 'proposal'}), Proposal)
    assert isinstance(discuss.instance({'kind': 'vote'}), Vote)


def test_get_post_facade(db_conn, posts_table):
    """
    Expect to get a post, and the instance to match the kind.
    """
    posts_table.insert({
        'id': 'fghj4567',
        'user_id': 'abcd1234',
        'topic_id': 'wxyz7890',
        'body': 'abcd',
        'kind': 'post',
    }).run(db_conn)
    assert isinstance(discuss.get_post_facade('fghj4567'), Post)


def test_get_posts_facade(db_conn, posts_table):
    """
    Expect to get a list of posts, and the instances to match the kinds.
    """
    posts_table.insert([{
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
    }]).run(db_conn)
    posts = discuss.get_posts_facade(topic_id='wxyz7890')
    assert isinstance(posts[0], Vote) or isinstance(posts[1], Vote)
    assert isinstance(posts[0], Post) and isinstance(posts[1], Post)


def test_create_post_facade(db_conn):
    """
    Expect to a create a post, and the right kind of instance.s
    """
    data = {
        'user_id': 'abcd1234',
        'topic_id': 'wxyz7890',
        'body': 'abcd',
        'kind': 'post',
    }
    post, errors = discuss.create_post_facade(data)
    assert len(errors) == 0
    assert isinstance(post, Post)
