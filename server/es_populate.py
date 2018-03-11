import psycopg2
import psycopg2.extras
from framework.database import make_db_connection, close_db_connection
from framework.elasticsearch_conn import es
from modules.util import json_prep, pick, convert_uuid_to_slug
from database.user import get_avatar


def es_populate():
  db_conn = make_db_connection()

  # Empty the database
  es.indices.delete(index='entity', ignore=[400, 404])

  # Add users
  cur = db_conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
  with cur:
    cur.execute("SELECT * FROM users;")
    data = cur.fetchall()
    users = [row for row in data]
    db_conn.commit()
  for user in users:
    data = pick(json_prep(user), ('id', 'name'))
    data['avatar'] = get_avatar(user['email'])
    es.index(
      index='entity',
      doc_type='user',
      body=data,
      id=convert_uuid_to_slug(user['id']),
    )

  # Add units
  cur = db_conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
  with cur:
    cur.execute("""
      SELECT DISTINCT ON (entity_id) *
      FROM units
      WHERE status = 'accepted'
      ORDER BY entity_id, created DESC;
    """)
    data = cur.fetchall()
    units = [row for row in data]
    db_conn.commit()
  for unit in units:
    es.index(
      index='entity',
      doc_type='unit',
      body=json_prep(unit),
      id=convert_uuid_to_slug(unit['entity_id']),
    )

  # Add cards
  cur = db_conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
  with cur:
    cur.execute("""
      SELECT DISTINCT ON (entity_id) *
      FROM cards
      WHERE status = 'accepted'
      ORDER BY entity_id, created DESC;
    """)
    data = cur.fetchall()
    cards = [row for row in data]
    db_conn.commit()
  for card in cards:
    es.index(
      index='entity',
      doc_type='card',
      body=json_prep(card),
      id=convert_uuid_to_slug(card['entity_id']),
    )

  # Add subjects
  cur = db_conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
  with cur:
    cur.execute("""
      SELECT DISTINCT ON (entity_id) *
      FROM subjects
      WHERE status = 'accepted'
      ORDER BY entity_id, created DESC;
    """)
    data = cur.fetchall()
    subjects = [row for row in data]
    db_conn.commit()
  for subject in subjects:
    es.index(
      index='entity',
      doc_type='subject',
      body=json_prep(subject),
      id=convert_uuid_to_slug(subject['entity_id']),
    )

  """
  TODO-1 fix these
  # Add topics
  topics = r.table('topics').run(db_conn)
  for topic in topics:
    es.index(
      index='entity',
      doc_type='topic',
      body=json_prep(topic),
      id=topic['id'],
    )

  # Add posts
  posts = r.table('posts').run(db_conn)
  for post in posts:
    data = json_prep(post)
    topic = (r.table('topics')
         .get(data['topic_id'])
         .run(db_conn))
    user = (r.table('users')
         .get(data['user_id'])
         .run(db_conn))
    data['topic'] = json_prep(topic)
    data['user'] = pick(json_prep(user), ('id', 'name'))
    es.index(
      index='entity',
      doc_type='post',
      body=data,
      id=post['id'],
    )
  """

  close_db_connection(db_conn)


if __name__ == "__main__":
  es_populate()
