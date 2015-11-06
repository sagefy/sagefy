from models.proposal import Proposal


def test_user_id(db_conn, posts_table):
    """
    Expect a proposal to require a user id.
    """

    proposal, errors = Proposal.insert({
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
    proposal, errors = proposal.save()
    assert len(errors) == 0


def test_topic(db_conn, posts_table):
    """
    Expect a proposal to require a topic id.
    """

    proposal, errors = Proposal.insert({
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
    proposal, errors = proposal.save()
    assert len(errors) == 0


def test_body(db_conn, posts_table):
    """
    Expect a proposal to require a body.
    """

    proposal, errors = Proposal.insert({
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
    proposal, errors = proposal.save()
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
    proposal, errors = proposal.save()
    assert len(errors) == 1
    proposal['kind'] = 'proposal'
    proposal, errors = proposal.save()
    assert len(errors) == 0


def test_replies(db_conn, posts_table):
    """
    Expect a proposal to allow a replies to id.
    """

    proposal, errors = Proposal.insert({
        'user_id': 'A',
        'topic_id': 'B',
        'body': 'C',
        'entity_version': {
            'id': 'D',
            'kind': 'unit'
        },
        'name': 'E',
        'replies_to_id': 'A',
    })
    assert len(errors) == 0


def test_entity(db_conn, posts_table):
    """
    Expect a proposal to require an entity version id.
    """

    proposal, errors = Proposal.insert({
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
    proposal, errors = proposal.save()
    assert len(errors) == 0


def test_name(db_conn, posts_table):
    """
    Expect a proposal to require a name.
    """

    proposal, errors = Proposal.insert({
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
    proposal, errors = proposal.save()
    assert len(errors) == 0