import uuid
from database.post import get_post_schema, \
  is_valid_reply, \
  validate_entity_versions, \
  is_valid_reply_kind, \
  insert_post, \
  insert_proposal, \
  insert_vote, \
  update_post, \
  update_proposal, \
  update_vote, \
  get_post, \
  list_posts_by_topic, \
  list_posts_by_user, \
  deliver_post, \
  add_post_to_es, \
  list_votes_by_proposal
from database.unit import update_unit
from raw_insert import raw_insert_users, \
  raw_insert_units, \
  raw_insert_topics, \
  raw_insert_posts
from modules.util import convert_uuid_to_slug



user_uuid = uuid.uuid4()
user_b_uuid = uuid.uuid4()
test_unit_uuid = uuid.uuid4()
test_unit_version_uuid = uuid.uuid4()
test_unit_b_uuid = uuid.uuid4()
test_unit_b_version_uuid = uuid.uuid4()
test_follow_a_id = uuid.uuid4()
test_topic_id = uuid.uuid4()
test_topic_b_id = uuid.uuid4()
proposal_uuid = uuid.uuid4()
post_uuid = uuid.uuid4()
vote_uuid = uuid.uuid4()


def create_test_posts(db_conn):
  users = [{
    'id': user_uuid,
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
    'version_id': test_unit_version_uuid,
    'user_id': user_uuid,
    'entity_id': test_unit_uuid,
    'name': 'test unit add',
    'body': 'adding numbers is fun',
  }, {
    'version_id': test_unit_b_version_uuid,
    'user_id': user_uuid,
    'entity_id': test_unit_b_uuid,
    'name': 'test unit subtract',
    'body': 'subtracting numbers is fun',
  }]
  raw_insert_units(db_conn, units)
  topics = [{
    'id': test_topic_id,
    'user_id': user_uuid,
    'entity_id': test_unit_uuid,
    'entity_kind': 'unit',
    'name': 'Lets talk about adding numbers',
  }, {
    'id': test_topic_b_id,
    'user_id': user_uuid,
    'entity_id': test_unit_b_uuid,
    'entity_kind': 'unit',
    'name': 'Lets talk about subtracting numbers',
  }]
  raw_insert_topics(db_conn, topics)
  posts = [{
    'id': proposal_uuid,
    'kind': 'proposal',
    'body': 'A new version',
    'entity_versions': [{
      'id': convert_uuid_to_slug(test_unit_version_uuid),
      'kind': 'unit',
    }],
    'user_id': user_uuid,
    'topic_id': test_topic_id,
  }, {
    'id': post_uuid,
    'kind': 'post',
    'body': 'I just love adding numbers.',
    'user_id': user_uuid,
    'topic_id': test_topic_id,
  }, {
    'id': vote_uuid,
    'kind': 'vote',
    'body': 'Yay!',
    'replies_to_id': proposal_uuid,
    'response': True,
    'user_id': user_b_uuid,
    'topic_id': test_topic_id,
  }]
  raw_insert_posts(db_conn, posts)


def test_get_post_schema():
  schema = get_post_schema({'kind': 'post'})
  assert schema
  assert schema['tablename'] == 'posts'


def test_is_valid_reply(db_conn):
  create_test_posts(db_conn)
  data = {}
  errors = is_valid_reply(db_conn, data)
  assert not errors
  data = {
    'topic_id': test_topic_id,
    'replies_to_id': uuid.uuid4()
  }
  errors = is_valid_reply(db_conn, data)
  assert errors
  data = {
    'replies_to_id': proposal_uuid
  }
  errors = is_valid_reply(db_conn, data)
  assert errors
  data = {
    'topic_id': test_topic_id,
    'replies_to_id': proposal_uuid
  }
  errors = is_valid_reply(db_conn, data)
  assert not errors


def test_validate_entity_versions(db_conn):
  create_test_posts(db_conn)
  data = {
    'entity_versions': [{
      'id': convert_uuid_to_slug(uuid.uuid4()),
      'kind': 'unit',
    }]
  }
  errors = validate_entity_versions(db_conn, data)
  assert errors
  data = {
    'entity_versions': [{
      'id': convert_uuid_to_slug(test_unit_version_uuid),
      'kind': 'unit',
    }]
  }
  errors = validate_entity_versions(db_conn, data)
  assert not errors


def test_is_valid_reply_kind(db_conn):
  create_test_posts(db_conn)
  # 1  Doesn't reply to anything
  data = {'replies_to_id': uuid.uuid4()}
  errors = is_valid_reply_kind(db_conn, data)
  assert errors[0]['message'] == 'No proposal found.'
  # 2  Doesn't reply to a proposal
  data = {'replies_to_id': post_uuid}
  errors = is_valid_reply_kind(db_conn, data)
  assert errors[0]['message'] == 'A vote must reply to a proposal.'
  # 3  Trying to vote on own proposal
  data = {
    'replies_to_id': proposal_uuid,
    'user_id': user_uuid,
  }
  errors = is_valid_reply_kind(db_conn, data)
  assert errors[0]['message'] == 'You cannot vote on your own proposal.'
  # 4  Voting on a proposal with no entity version
  bad_proposal_uuid = uuid.uuid4()
  posts = [{
    'id': bad_proposal_uuid,
    'kind': 'proposal',
    'body': 'A new version',
    'entity_versions': [{
      'id': convert_uuid_to_slug(uuid.uuid4()),
      'kind': 'unit',
    }],
    'user_id': user_uuid,
    'topic_id': test_topic_id,
  }]
  raw_insert_posts(db_conn, posts)
  data = {
    'replies_to_id': bad_proposal_uuid,
    'user_id': user_b_uuid,
  }
  errors = is_valid_reply_kind(db_conn, data)
  assert errors[0]['message'] == 'No entity version for proposal.'
  # 5  Voting on a an already complete proposal
  data = {
    'replies_to_id': proposal_uuid,
    'user_id': user_b_uuid,
  }
  errors = is_valid_reply_kind(db_conn, data)
  assert errors[0]['message'] == 'Proposal is already complete.'
  # 6  Voting a on a valid proposal
  update_unit(db_conn, test_unit_version_uuid, status='pending')
  data = {
    'replies_to_id': proposal_uuid,
    'user_id': user_b_uuid,
  }
  errors = is_valid_reply_kind(db_conn, data)
  assert not errors


def test_insert_post(db_conn):
  create_test_posts(db_conn)
  data = {
    'user_id': user_b_uuid,
    'topic_id': test_topic_b_id,
    'body': 'Isnt this fun?',
    'replies_to_id': uuid.uuid4(),
  }
  post, errors = insert_post(db_conn, data)
  assert errors
  assert not post
  data = {
    'user_id': user_b_uuid,
    'topic_id': test_topic_b_id,
    'body': 'Isnt this fun?',
  }
  post, errors = insert_post(db_conn, data)
  assert not errors
  assert post


def test_insert_proposal(db_conn):
  create_test_posts(db_conn)
  data = {
    'user_id': user_b_uuid,
    'topic_id': test_topic_b_id,
    'body': 'A new thing',
    'entity_versions': [{
      'id': convert_uuid_to_slug(test_unit_version_uuid),
      'kind': 'unit',
    }],
    'replies_to_id': uuid.uuid4(),
  }
  proposal, errors = insert_proposal(db_conn, data)
  assert errors
  assert not proposal
  data = {
    'user_id': user_b_uuid,
    'topic_id': test_topic_b_id,
    'body': 'A new thing',
    'entity_versions': [{
      'id': convert_uuid_to_slug(uuid.uuid4()),
      'kind': 'unit',
    }],
  }
  proposal, errors = insert_proposal(db_conn, data)
  assert errors
  assert not proposal
  data = {
    'user_id': user_b_uuid,
    'topic_id': test_topic_b_id,
    'body': 'A new thing',
    'entity_versions': [{
      'id': convert_uuid_to_slug(test_unit_version_uuid),
      'kind': 'unit',
    }],
  }
  proposal, errors = insert_proposal(db_conn, data)
  assert not errors
  assert proposal


def test_insert_vote(db_conn):
  create_test_posts(db_conn)
  update_unit(db_conn, test_unit_version_uuid, status='pending')
  data = {
    'user_id': user_b_uuid,
    'topic_id': test_topic_b_id,
    'body': 'A new thing',
    'entity_versions': [{
      'id': convert_uuid_to_slug(test_unit_version_uuid),
      'kind': 'unit',
    }],
  }
  proposal, errors = insert_proposal(db_conn, data)
  assert not errors
  data = {
    'user_id': user_uuid,
    'topic_id': test_topic_b_id,
    'body': 'Boo!',
    'replies_to_id': uuid.uuid4(),
    'response': False,
  }
  vote, errors = insert_vote(db_conn, data)
  assert errors
  assert not vote
  data = {
    'user_id': user_b_uuid,
    'topic_id': test_topic_b_id,
    'body': 'Boo!',
    'replies_to_id': proposal['id'],
    'response': False,
  }
  vote, errors = insert_vote(db_conn, data)
  assert errors
  assert not vote
  data = {
    'user_id': user_uuid,
    'topic_id': test_topic_b_id,
    'body': 'Boo!',
    'replies_to_id': proposal['id'],
    'response': False,
  }
  vote, errors = insert_vote(db_conn, data)
  assert not errors
  assert vote


def test_update_post(db_conn):
  create_test_posts(db_conn)
  prev_data = get_post(db_conn, {
    'id': post_uuid,
  })
  data = {
    'body': 'This is a great post.'
  }
  post, errors = update_post(db_conn, prev_data, data)
  assert not errors
  assert post


def test_update_proposal(db_conn):
  create_test_posts(db_conn)
  prev_data = get_post(db_conn, {
    'id': proposal_uuid,
  })
  data = {
    'body': 'This is a great proposal.'
  }
  proposal, errors = update_proposal(db_conn, prev_data, data)
  assert not errors
  assert proposal


def test_update_vote(db_conn):
  create_test_posts(db_conn)
  prev_data = get_post(db_conn, {
    'id': vote_uuid,
  })
  data = {
    'body': 'Updated body',
    'response': False,
  }
  vote, errors = update_vote(db_conn, prev_data, data)
  assert not errors
  assert vote


def test_get_post(db_conn):
  create_test_posts(db_conn)
  params = {
    'id': proposal_uuid,
  }
  assert get_post(db_conn, params)


def test_list_posts_by_topic(db_conn):
  create_test_posts(db_conn)
  params = {
    'topic_id': test_topic_id
  }
  posts = list_posts_by_topic(db_conn, params)
  assert posts
  assert len(posts) == 3
  assert posts[0]['topic_id'] == test_topic_id
  assert posts[1]['topic_id'] == test_topic_id
  assert posts[2]['topic_id'] == test_topic_id


def test_list_posts_by_user(db_conn):
  create_test_posts(db_conn)
  params = {
    'user_id': user_uuid
  }
  posts = list_posts_by_user(db_conn, params)
  assert posts
  assert len(posts) == 2
  assert posts[0]['user_id'] == user_uuid
  assert posts[1]['user_id'] == user_uuid


def test_deliver_post(db_conn):
  create_test_posts(db_conn)
  data = get_post(db_conn, {
    'id': post_uuid,
  })
  assert deliver_post(data, access=None)


def test_add_post_to_es(db_conn):
  create_test_posts(db_conn)
  post = get_post(db_conn, {
    'id': post_uuid,
  })
  assert add_post_to_es(db_conn, post)


def test_list_votes_by_proposal(db_conn):
  create_test_posts(db_conn)
  votes = list_votes_by_proposal(db_conn, proposal_uuid)
  assert votes
  assert len(votes) == 1
  assert votes[0]['replies_to_id'] == proposal_uuid
