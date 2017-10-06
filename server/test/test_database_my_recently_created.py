from database.my_recently_created import get_my_recent_proposals, \
    get_proposal_entity_versions, \
    get_my_recently_created_units, \
    get_my_recently_created_subjects
from raw_insert import raw_insert_users, \
    raw_insert_topics, \
    raw_insert_posts, \
    raw_insert_units, \
    raw_insert_subjects
import uuid
from modules.util import convert_uuid_to_slug
from database.user import get_user_by_id

user_a_uuid = uuid.uuid4()
user_b_uuid = uuid.uuid4()
unit_a_uuid = uuid.uuid4()
unit_version_a_uuid = uuid.uuid4()
subject_a_uuid = uuid.uuid4()
subject_version_a_uuid = uuid.uuid4()
topic_a_uuid = uuid.uuid4()
topic_b_uuid = uuid.uuid4()
proposal_a_uuid = uuid.uuid4()
proposal_b_uuid = uuid.uuid4()


def create_my_recent_test_data(db_conn):
    users = [{
        'id': user_a_uuid,
        'name': 'test',
        'email': 'test@example.com',
        'password': 'abcd1234',
    }, {
        'id': user_b_uuid,
        'name': 'other',
        'email': 'other@example.com',
        'password': 'abcd1234',
    }]
    raw_insert_users(db_conn, users)
    units = [{
        'version_id': unit_version_a_uuid,
        'user_id': user_a_uuid,
        'entity_id': unit_a_uuid,
        'name': 'test unit add',
        'body': 'adding numbers is fun',
    }]
    raw_insert_units(db_conn, units)
    subjects = [{
        'version_id': subject_version_a_uuid,
        'entity_id': subject_a_uuid,
        'name': 'Math',
        'user_id': user_a_uuid,
        'body': 'Math is fun.',
        'members': [{
            'kind': 'unit',
            'id': convert_uuid_to_slug(unit_a_uuid),
        }],
    }]
    raw_insert_subjects(db_conn, subjects)
    topics = [{
        'id': topic_a_uuid,
        'user_id': user_a_uuid,
        'entity_id': unit_a_uuid,
        'entity_kind': 'unit',
        'name': 'Lets talk about adding numbers',
    }, {
        'id': topic_b_uuid,
        'user_id': user_a_uuid,
        'entity_id': subject_a_uuid,
        'entity_kind': 'subject',
        'name': 'Lets talk about subtracting numbers',
    }]
    raw_insert_topics(db_conn, topics)
    posts = [{
        'id': proposal_a_uuid,
        'kind': 'proposal',
        'body': 'A new unit version',
        'entity_versions': [{
            'id': convert_uuid_to_slug(unit_version_a_uuid),
            'kind': 'unit',
        }],
        'user_id': user_a_uuid,
        'topic_id': topic_a_uuid,
    }, {
        'id': proposal_b_uuid,
        'kind': 'proposal',
        'body': 'A new subjectversion',
        'entity_versions': [{
            'id': convert_uuid_to_slug(subject_version_a_uuid),
            'kind': 'subject',
        }],
        'user_id': user_a_uuid,
        'topic_id': topic_b_uuid,
    }]
    raw_insert_posts(db_conn, posts)


def test_get_my_recent_proposals(db_conn):
    create_my_recent_test_data(db_conn)
    current_user = get_user_by_id(db_conn, {'id': user_a_uuid})
    proposals = get_my_recent_proposals(db_conn, current_user)
    assert proposals
    assert len(proposals) == 2
    assert proposals[0]['user_id'] == user_a_uuid
    assert proposals[1]['user_id'] == user_a_uuid


def test_get_proposal_entity_versions(db_conn):
    create_my_recent_test_data(db_conn)
    current_user = get_user_by_id(db_conn, {'id': user_a_uuid})
    proposals = get_my_recent_proposals(db_conn, current_user)
    unit_evs = get_proposal_entity_versions(proposals, 'unit')
    assert unit_evs
    assert len(unit_evs) == 1
    sub_evs = get_proposal_entity_versions(proposals, 'subject')
    assert sub_evs
    assert len(sub_evs) == 1


def test_get_my_recently_created_units(db_conn):
    create_my_recent_test_data(db_conn)
    current_user = get_user_by_id(db_conn, {'id': user_a_uuid})
    units = get_my_recently_created_units(db_conn, current_user)
    assert units
    assert len(units) == 1
    assert units[0]['user_id'] == user_a_uuid


def test_get_my_recently_created_subjects(db_conn):
    create_my_recent_test_data(db_conn)
    current_user = get_user_by_id(db_conn, {'id': user_a_uuid})
    subjects = get_my_recently_created_subjects(db_conn, current_user)
    assert subjects
    assert len(subjects) == 1
    assert subjects[0]['user_id'] == user_a_uuid
