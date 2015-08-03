from models.proposal import Proposal


def test_user_id(db_conn, posts_table):
    """
    Expect a proposal to require a user id.
    """

    proposal, errors = Proposal.insert({
        'topic_id': 'B',
        'body': 'C',
        'entity_version_id': 'D',
        'name': 'E',
        'status': 'pending',
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
        'entity_version_id': 'D',
        'name': 'E',
        'status': 'pending',
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
        'entity_version_id': 'D',
        'name': 'E',
        'status': 'pending',
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
        'entity_version_id': 'D',
        'name': 'E',
        'status': 'pending',
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
        'entity_version_id': 'D',
        'name': 'E',
        'status': 'pending',
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
        'status': 'pending',
    })
    assert len(errors) == 1
    proposal['entity_version_id'] = 'D'
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
        'entity_version_id': 'D',
        'status': 'pending',
    })
    assert len(errors) == 1
    proposal['name'] = 'E'
    proposal, errors = proposal.save()
    assert len(errors) == 0


def test_status(db_conn, posts_table):
    """
    Expect a proposal to require a status.
    """

    proposal = Proposal({
        'user_id': 'A',
        'topic_id': 'B',
        'body': 'C',
        'entity_version_id': 'D',
        'name': 'E',
    })
    assert proposal['status'] == 'pending'
    del proposal['status']
    proposal, errors = proposal.save()
    assert len(errors) == 1
    proposal['status'] = 'pending'
    proposal, errors = proposal.save()
    assert len(errors) == 0
