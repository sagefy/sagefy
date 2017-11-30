from datetime import datetime
import uuid
from modules.sequencer.params import precision
from modules.util import convert_slug_to_uuid, convert_uuid_to_slug
import psycopg2.extras
from database.util import save_row
from passlib.hash import bcrypt
from conftest import user_id


def raw_insert_users(db_conn, users):
  for user in users:
    query = """
      INSERT INTO users
      (  id  ,   created  ,   modified  ,
         name  ,   email  ,   password  ,   settings)
      VALUES
      (%(id)s, %(created)s, %(modified)s,
       %(name)s, %(email)s, %(password)s, %(settings)s)
      RETURNING *;
    """
    params = {
      'id': user.get('id', uuid.uuid4()),
      'created': user.get('created', datetime.utcnow()),
      'modified': user.get('modified', datetime.utcnow()),
      'name': user.get('name'),
      'email': user.get('email'),
      # NOTE do not set rounds this low in production!
      'password': bcrypt.encrypt(user.get('password'), rounds=4),
      'settings': psycopg2.extras.Json(user.get('settings', {
        'email_frequency': 'daily',
        'view_subjects': 'public',
        'view_follows': 'public',
      })),
    }
    save_row(db_conn, query, params)


def raw_insert_cards(db_conn, cards):
  for card in cards:
    query = """
      INSERT INTO cards_entity_id (entity_id)
      VALUES (%(entity_id)s)
      ON CONFLICT DO NOTHING;
      INSERT INTO cards
      (  version_id  ,   created  ,   modified  ,
         entity_id  ,   previous_id  ,   language  ,   status  ,
         available  ,   tags  ,   name  ,   user_id  ,
         unit_id  ,   require_ids  ,   kind  ,   data  )
      VALUES
      (%(version_id)s, %(created)s, %(modified)s,
       %(entity_id)s, %(previous_id)s, %(language)s, %(status)s,
       %(available)s, %(tags)s, %(name)s, %(user_id)s,
       %(unit_id)s, %(require_ids)s, %(kind)s, %(data)s)
      RETURNING *;
    """
    params = {
      'version_id': card.get('version_id', uuid.uuid4()),
      'created': card.get('created', datetime.utcnow()),
      'modified': card.get('modified', datetime.utcnow()),
      'entity_id': card.get('entity_id'),
      'previous_id': card.get('previous_id'),
      'language': card.get('language', 'en'),
      'status': card.get('status', 'accepted'),
      'available': card.get('available', True),
      'tags': card.get('tags', []),
      'name': card.get('name'),
      'user_id': card.get('user_id', convert_slug_to_uuid(user_id)),
      'unit_id': card.get('unit_id'),
      'require_ids': card.get('require_ids', []),
      'kind': card.get('kind'),
      'data': psycopg2.extras.Json(card.get('data', {})),
    }
    save_row(db_conn, query, params)
    if card.get('kind') == 'choice':
      query = """
        INSERT INTO cards_parameters
        (  entity_id  ,   guess_distribution  ,   slip_distribution  )
        VALUES
        (%(entity_id)s, %(guess_distribution)s, %(slip_distribution)s)
        RETURNING *;
      """
      params = {
        'entity_id': card.get('entity_id'),
        'guess_distribution': psycopg2.extras.Json({
          str(h): 1 - (0.5 - h) ** 2
          for h in [h / precision for h in range(1, precision)]
        }),
        'slip_distribution': psycopg2.extras.Json({
          str(h): 1 - (0.25 - h) ** 2
          for h in [h / precision for h in range(1, precision)]
        }),
      }
      save_row(db_conn, query, params)


def raw_insert_units(db_conn, units):
  for unit in units:
    query = """
      INSERT INTO units_entity_id (entity_id)
      VALUES (%(entity_id)s)
      ON CONFLICT DO NOTHING;
      INSERT INTO units
      (  version_id  ,   created  ,   modified  ,
         entity_id  ,   previous_id  ,   language  ,   status  ,
         available  ,   tags  ,   name  ,   user_id  ,
         body  ,   require_ids  )
      VALUES
      (%(version_id)s, %(created)s, %(modified)s,
       %(entity_id)s, %(previous_id)s, %(language)s, %(status)s,
       %(available)s, %(tags)s, %(name)s, %(user_id)s,
       %(body)s, %(require_ids)s)
      RETURNING *;
    """
    params = {
      'version_id': unit.get('version_id', uuid.uuid4()),
      'created': unit.get('created', datetime.utcnow()),
      'modified': unit.get('modified', datetime.utcnow()),
      'entity_id': unit.get('entity_id'),
      'previous_id': unit.get('previous_id'),
      'language': unit.get('language', 'en'),
      'status': unit.get('status', 'accepted'),
      'available': unit.get('available', True),
      'tags': unit.get('tags', []),
      'name': unit.get('name'),
      'user_id': unit.get('user_id', convert_slug_to_uuid(user_id)),
      'body': unit.get('body'),
      'require_ids': unit.get('require_ids', []),
    }
    save_row(db_conn, query, params)


def raw_insert_subjects(db_conn, subjects):
  for subject in subjects:
    query = """
      INSERT INTO subjects_entity_id (entity_id)
      VALUES (%(entity_id)s)
      ON CONFLICT DO NOTHING;
      INSERT INTO subjects
      (  version_id  ,   created  ,   modified  ,
         entity_id  ,   previous_id  ,   language  ,   status  ,
         available  ,   tags  ,   name  ,   user_id  ,
         body  ,   members  )
      VALUES
      (%(version_id)s, %(created)s, %(modified)s,
       %(entity_id)s, %(previous_id)s, %(language)s, %(status)s,
       %(available)s, %(tags)s, %(name)s, %(user_id)s,
       %(body)s, %(members)s)
      RETURNING *;
    """
    params = {
      'version_id': subject.get('version_id', uuid.uuid4()),
      'created': subject.get('created', datetime.utcnow()),
      'modified': subject.get('modified', datetime.utcnow()),
      'entity_id': subject.get('entity_id'),
      'previous_id': subject.get('previous_id'),
      'language': subject.get('language', 'en'),
      'status': subject.get('status', 'accepted'),
      'available': subject.get('available', True),
      'tags': subject.get('tags', []),
      'name': subject.get('name'),
      'user_id': subject.get('user_id', convert_slug_to_uuid(user_id)),
      'body': subject.get('body'),
      'members': psycopg2.extras.Json(
        subject.get('members', [])
      ),
    }
    save_row(db_conn, query, params)


def raw_insert_topics(db_conn, topics):
  for topic in topics:
    query = """
      INSERT INTO topics
      (  id, created, modified,
         user_id, name, entity_id, entity_kind)
      VALUES
      (%(id)s, %(created)s, %(modified)s,
       %(user_id)s, %(name)s, %(entity_id)s, %(entity_kind)s)
      RETURNING *;
    """
    params = {
      'id': topic.get('id', uuid.uuid4()),
      'created': topic.get('created', datetime.utcnow()),
      'modified': topic.get('modified', datetime.utcnow()),
      'user_id': topic.get('user_id'),
      'name': topic.get('name'),
      'entity_id': topic.get('entity_id'),
      'entity_kind': topic.get('entity_kind'),
    }
    save_row(db_conn, query, params)


def raw_insert_posts(db_conn, posts):
  for post in posts:
    query = """
      INSERT INTO posts
      (id, created, modified,
       kind, body, replies_to_id,
       entity_versions, response, user_id,
       topic_id)
      VALUES
      (%(id)s, %(created)s, %(modified)s,
       %(kind)s, %(body)s, %(replies_to_id)s,
       %(entity_versions)s, %(response)s, %(user_id)s,
       %(topic_id)s)
      RETURNING *;
    """
    params = {
      'id': post.get('id', uuid.uuid4()),
      'created': post.get('created', datetime.utcnow()),
      'modified': post.get('modified', datetime.utcnow()),
      'kind': post.get('kind'),
      'body': post.get('body'),
      'replies_to_id': post.get('replies_to_id'),
      'entity_versions': psycopg2.extras.Json(
        post.get('entity_versions', [])
      ),
      'response': post.get('response'),
      'user_id': post.get('user_id'),
      'topic_id': post.get('topic_id'),
    }
    save_row(db_conn, query, params)


def raw_insert_follows(db_conn, follows):
  for follow in follows:
    query = """
      INSERT INTO follows
      (id, created, modified,
       user_id, entity_id, entity_kind)
      VALUES
      (%(id)s, %(created)s, %(modified)s,
       %(user_id)s, %(entity_id)s, %(entity_kind)s)
      RETURNING *;
    """
    params = {
      'id': follow.get('id', uuid.uuid4()),
      'created': follow.get('created', datetime.utcnow()),
      'modified': follow.get('modified', datetime.utcnow()),
      'user_id': follow.get('user_id'),
      'entity_id': follow.get('entity_id'),
      'entity_kind': follow.get('entity_kind'),
    }
    save_row(db_conn, query, params)


def raw_insert_notices(db_conn, notices):
  for notice in notices:
    query = """
      INSERT INTO notices
      (id, created, modified,
       user_id, kind, data, read, tags)
      VALUES
      (%(id)s, %(created)s, %(modified)s,
       %(user_id)s, %(kind)s, %(data)s, %(read)s, %(tags)s)
      RETURNING *;
    """
    params = {
      'id': notice.get('id', uuid.uuid4()),
      'created': notice.get('created', datetime.utcnow()),
      'modified': notice.get('modified', datetime.utcnow()),
      'user_id': notice.get('user_id'),
      'kind': notice.get('kind'),
      'data': psycopg2.extras.Json(
        notice.get('data', {})
      ),
      'read': notice.get('read', False),
      'tags': notice.get('tags', []),
    }
    save_row(db_conn, query, params)


def raw_insert_user_subjects(db_conn, user_subjects):
  for user_subject in user_subjects:
    query = """
      INSERT INTO users_subjects
      (id, created, modified,
       user_id, subject_id)
      VALUES
      (%(id)s, %(created)s, %(modified)s,
       %(user_id)s, %(subject_id)s)
      RETURNING *;
    """
    params = {
      'id': user_subject.get('id', uuid.uuid4()),
      'created': user_subject.get('created', datetime.utcnow()),
      'modified': user_subject.get('modified', datetime.utcnow()),
      'user_id': user_subject.get('user_id'),
      'subject_id': user_subject.get('subject_id'),
    }
    save_row(db_conn, query, params)


def raw_insert_responses(db_conn, responses):
  for response in responses:
    query = """
      INSERT INTO responses
      (id, created, modified,
       user_id, card_id, unit_id,
       response, score, learned)
      VALUES
      (%(id)s, %(created)s, %(modified)s,
       %(user_id)s, %(card_id)s, %(unit_id)s,
       %(response)s, %(score)s, %(learned)s)
      RETURNING *;
    """
    params = {
      'id': response.get('id', uuid.uuid4()),
      'created': response.get('created', datetime.utcnow()),
      'modified': response.get('modified', datetime.utcnow()),
      'user_id': convert_slug_to_uuid(response.get('user_id')),
      'card_id': convert_slug_to_uuid(response.get('card_id')),
      'unit_id': convert_slug_to_uuid(response.get('unit_id')),
      'response': convert_uuid_to_slug(response.get('response')),
      'score': response.get('score'),
      'learned': response.get('learned'),
    }
    save_row(db_conn, query, params)
