from models.proposal import Proposal
from models.post import Post


def test_user_id(db_conn, posts_table):
    """
    Expect a proposal to require a user id.
    """

    proposal, errors = Proposal.insert(db_conn, {
        'topic_id': 'B',
        'body': 'C',
        'entity_version': {
            'id': 'D',
            'kind': 'unit'
        },
        'name': 'E',
    })
    assert len(errors) == 1
    proposal['user_id'] = 'A'
    proposal, errors = proposal.save(db_conn)
    assert len(errors) == 0


def test_topic(db_conn, posts_table):
    """
    Expect a proposal to require a topic id.
    """

    proposal, errors = Proposal.insert(db_conn, {
        'user_id': 'A',
        'body': 'C',
        'entity_version': {
            'id': 'D',
            'kind': 'unit'
        },
        'name': 'E',
    })
    assert len(errors) == 1
    proposal['topic_id'] = 'B'
    proposal, errors = proposal.save(db_conn)
    assert len(errors) == 0


def test_body(db_conn, posts_table):
    """
    Expect a proposal to require a body.
    """

    proposal, errors = Proposal.insert(db_conn, {
        'user_id': 'A',
        'topic_id': 'B',
        'entity_version': {
            'id': 'D',
            'kind': 'unit'
        },
        'name': 'E',
    })
    assert len(errors) == 1
    proposal['body'] = 'C'
    proposal, errors = proposal.save(db_conn)
    assert len(errors) == 0


def test_kind(db_conn, posts_table):
    """
    Expect a proposal to have a kind.
    """

    proposal = Proposal({
        'user_id': 'A',
        'topic_id': 'B',
        'body': 'C',
        'entity_version': {
            'id': 'D',
            'kind': 'unit'
        },
        'name': 'E',
    })
    del proposal['kind']
    proposal, errors = proposal.save(db_conn)
    assert len(errors) == 1
    proposal['kind'] = 'proposal'
    proposal, errors = proposal.save(db_conn)
    assert len(errors) == 0


def test_replies(db_conn, posts_table):
    """
    Expect a proposal to allow a replies to id.
    """

    prev, errors = Post.insert(db_conn, {
        'user_id': 'A',
        'topic_id': 'B',
        'body': 'C',
    })
    proposal, errors = Proposal.insert(db_conn, {
        'user_id': 'A',
        'topic_id': 'B',
        'body': 'C',
        'entity_version': {
            'id': 'D',
            'kind': 'unit'
        },
        'name': 'E',
        'replies_to_id': prev['id'],
    })
    assert len(errors) == 0


def test_entity(db_conn, posts_table):
    """
    Expect a proposal to require an entity version id.
    """

    proposal, errors = Proposal.insert(db_conn, {
        'user_id': 'A',
        'topic_id': 'B',
        'body': 'C',
        'name': 'E',
    })
    assert len(errors) == 2
    proposal['entity_version'] = {
        'id': 'D',
        'kind': 'unit'
    }
    proposal, errors = proposal.save(db_conn)
    assert len(errors) == 0


def test_name(db_conn, posts_table):
    """
    Expect a proposal to require a name.
    """

    proposal, errors = Proposal.insert(db_conn, {
        'user_id': 'A',
        'topic_id': 'B',
        'body': 'C',
        'entity_version': {
            'id': 'D',
            'kind': 'unit'
        }
    })
    assert len(errors) == 1
    proposal['name'] = 'E'
    proposal, errors = proposal.save(db_conn)
    assert len(errors) == 0
