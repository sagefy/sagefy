from database.user_subjects import insert_user_subjects, \
    list_user_subjects_entity
# get_user_subjects, append_user_subjects, remove_user_subjects,



def test_user(db_conn, users_subjects_table):
    """
    Expect to require a user ID.
    """

    user_subject_data = {
        'subject_ids': [
            'A',
            'B',
        ],
    }
    user_subjects, errors = insert_user_subjects(db_conn, user_subject_data)
    assert len(errors) == 1
    user_subject_data['user_id'] = 'A'
    user_subjects, errors = insert_user_subjects(db_conn, user_subject_data)
    assert len(errors) == 0


def test_subjects(db_conn, users_subjects_table):
    """
    Expect to require a list of subject IDs.
    """

    user_subject_data = {
        'user_id': 'A'
    }
    user_subjects, errors = insert_user_subjects(db_conn, user_subject_data)
    assert len(errors) == 1
    user_subject_data['subject_ids'] = [
        'A',
        'B',
    ]
    user_subjects, errors = insert_user_subjects(db_conn, user_subject_data)
    assert len(errors) == 0


def test_list_subjects(db_conn, users_subjects_table, subjects_table):
    """
    Expect to list subjects a user subscribes to.
    """

    subjects_table.insert([{
        'entity_id': 'A1',
        'name': 'A',
        'body': 'Apple',
        'created': datetime.utcnow(),
        'modified': datetime.utcnow(),
        'status': 'accepted',
    }, {
        'entity_id': 'B2',
        'name': 'B',
        'body': 'Banana',
        'created': datetime.utcnow(),
        'modified': datetime.utcnow(),
        'status': 'accepted',
    }, {
        'entity_id': 'C3',
        'name': 'C',
        'body': 'Coconut',
        'created': datetime.utcnow(),
        'modified': datetime.utcnow(),
        'status': 'accepted',
    }, {
        'entity_id': 'D4',
        'name': 'D',
        'body': 'Date',
        'created': datetime.utcnow(),
        'modified': datetime.utcnow(),
        'status': 'accepted',
    }]).run(db_conn)
    users_subjects_table.insert({
        'user_id': 'abcd1234',
        'subject_ids': [
            'A1',
            'C3',
        ],
        'created': datetime.utcnow(),
        'modified': datetime.utcnow(),
    }).run(db_conn)
    user_id = 'abcd1234'
    subjects = list_user_subjects_entity(db_conn, user_id, {})
    assert subjects[0]['body'] in ('Apple', 'Coconut')
    assert subjects[1]['body'] in ('Apple', 'Coconut')
