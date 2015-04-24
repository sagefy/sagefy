from models.flag import Flag


def test_user_id(db_conn, posts_table):
    """
    Expect a flag to require a user id.
    """

    flag, errors = Flag.insert({
        'topic_id': 'B',
        'body': 'C',
        'reason': 'offensive',
        'status': 'pending',
    })
    assert len(errors) == 1
    flag['user_id'] = 'A'
    flag, errors = flag.save()
    assert len(errors) == 0


def test_topic_id(db_conn, posts_table):
    """
    Expect a flag to require a topic id.
    """

    flag, errors = Flag.insert({
        'user_id': 'A',
        'body': 'C',
        'reason': 'offensive',
        'status': 'pending',
    })
    assert len(errors) == 1
    flag['topic_id'] = 'B'
    flag, errors = flag.save()
    assert len(errors) == 0


def test_body(db_conn, posts_table):
    """
    Expect a flag to require a body.
    """

    flag, errors = Flag.insert({
        'user_id': 'A',
        'topic_id': 'B',
        'reason': 'offensive',
        'status': 'pending',
    })
    assert len(errors) == 1
    flag['body'] = 'C'
    flag, errors = flag.save()
    assert len(errors) == 0


def test_kind(db_conn, posts_table):
    """
    Expect a flag to have a kind.
    """

    flag = Flag({
        'user_id': 'A',
        'topic_id': 'B',
        'body': 'C',
        'reason': 'offensive',
        'status': 'pending',
    })
    del flag['kind']
    flag, errors = flag.save()
    assert len(errors) == 1
    flag['kind'] = 'flag'
    flag, errors = flag.save()
    assert len(errors) == 0


def test_replies(db_conn, posts_table):
    """
    Expect a flag to allow a replies to id.
    """

    flag, errors = Flag.insert({
        'user_id': 'A',
        'topic_id': 'B',
        'body': 'C',
        'reason': 'offensive',
        'status': 'pending',
    })
    assert len(errors) == 0
    flag['replies_to_id'] = 'D'
    flag, errors = flag.save()
    assert len(errors) == 0


def test_reason(db_conn, posts_table):
    """
    Expect a flag to require a reason.
    """

    flag, errors = Flag.insert({
        'user_id': 'A',
        'topic_id': 'B',
        'body': 'C',
        'status': 'pending',
    })
    assert len(errors) == 1
    flag['reason'] = 'offensive'
    flag, errors = flag.save()
    assert len(errors) == 0


def test_status(db_conn, posts_table):
    """
    Expect a flag to require a status.
    """

    flag, errors = Flag.insert({
        'user_id': 'A',
        'topic_id': 'B',
        'body': 'C',
        'reason': 'offensive',
    })
    assert flag['status'] == 'pending'  # Default value
    assert len(errors) == 0
    del flag['status']
    flag, errors = flag.save()
    assert len(errors) == 1
