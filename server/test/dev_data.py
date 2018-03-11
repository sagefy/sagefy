# pylint: disable=wrong-import-position,wrong-import-order

import uuid
from datetime import datetime, timezone
import yaml
import psycopg2
import psycopg2.extras

# via https://stackoverflow.com/a/11158224
import os
import sys
import inspect
currentdir = os.path.dirname(
  os.path.abspath(
    inspect.getfile(
      inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)


from config import config
from framework.database import make_db_connection, \
  close_db_connection
from framework.elasticsearch_conn import es
from framework.redis_conn import red
from test.raw_insert import raw_insert_users, raw_insert_cards, \
  raw_insert_units, raw_insert_subjects, raw_insert_topics, \
  raw_insert_posts, raw_insert_follows, raw_insert_notices
from es_populate import es_populate
from modules.util import convert_uuid_to_slug
from database.util import delete_row


if not config['debug']:
  raise Exception('You must be in debug mode to wipe the DB.')

psycopg2.extras.register_uuid()
db_conn = make_db_connection()


tablenames = (
  'users',
  'units_entity_id',
  'units',
  'cards_entity_id',
  'cards',
  'cards_parameters',
  'subjects_entity_id',
  'subjects',
  'topics',
  'posts',
  'follows',
  'notices',
  'users_subjects',
  'responses',
)

for tablename in reversed(tablenames):
  cur = db_conn.cursor()
  with cur:
    cur.execute("DELETE FROM {tablename};".format(tablename=tablename))
    db_conn.commit()

es.indices.delete(index='entity', ignore=[400, 404])

red.flushall()

stream = open('/www/intro_electronic_music_example_collection.yaml', 'r')
sample_data = yaml.load(stream)
stream.close()

doris_id = uuid.uuid4()
eileen_id = uuid.uuid4()

users = [{
  'id': doris_id,
  'created': datetime(2014, 1, 1, tzinfo=timezone.utc),
  'modified': datetime(2014, 1, 1, tzinfo=timezone.utc),
  'name': 'doris',
  'email': 'doris@example.com',
  'password': 'example1',
  'settings': {
    'email_frequency': 'daily',
    'view_subjects': 'public',
    'view_follows': 'public',
  },
}, {
  'id': eileen_id,
  'created': datetime(2014, 1, 1, tzinfo=timezone.utc),
  'modified': datetime(2014, 1, 1, tzinfo=timezone.utc),
  'name': 'eileen',
  'email': 'eileen@example.com',
  'password': 'example1',
  'settings': {
    'email_frequency': 'daily',
    'view_subjects': 'public',
    'view_follows': 'public',
  },
}]
raw_insert_users(db_conn, users)


# We have to translate the sample IDs to UUIDs
entity_ids_lookup = {}

# Dropping foreign key checks so the ordering doesn't matter.
query = """
  ALTER TABLE units DISABLE TRIGGER ALL;
"""
delete_row(db_conn, query, {})

for sample_id, unit_data in sample_data['units'].items():
  unit_data['version_id'] = uuid.uuid4()
  if sample_id in entity_ids_lookup:
    unit_data['entity_id'] = entity_ids_lookup[sample_id]
  else:
    unit_data['entity_id'] = entity_ids_lookup[sample_id] = uuid.uuid4()

  u_require_ids = []
  for id_ in unit_data['require_ids']:
    if id_ not in entity_ids_lookup:
      entity_ids_lookup[id_] = uuid.uuid4()
    u_require_ids.append(entity_ids_lookup[id_])
  unit_data['require_ids'] = u_require_ids

  params = {
    'version_id': unit_data['version_id'],
    'created': datetime(2014, 1, 1, tzinfo=timezone.utc),
    'modified': datetime(2014, 1, 1, tzinfo=timezone.utc),
    'entity_id': unit_data['entity_id'],
    'previous_id': None,
    # 'language': 'en',
    # 'status': 'accepted',
    # 'available': True,
    # 'tags': [],
    'name': unit_data['name'],
    'user_id': doris_id,
    'body': unit_data['body'],
    'require_ids': unit_data['require_ids'],
  }
  raw_insert_units(db_conn, [params])

query = """
  ALTER TABLE units ENABLE TRIGGER ALL;
"""
delete_row(db_conn, query, {})

for card_data in sample_data['cards']['video']:
  card_data['entity_id'] = uuid.uuid4()
  params = {
    'version_id': uuid.uuid4(),
    'created': datetime(2014, 1, 1, tzinfo=timezone.utc),
    'modified': datetime(2014, 1, 1, tzinfo=timezone.utc),
    'entity_id': card_data['entity_id'],
    'previous_id': None,
    # 'language': 'en',
    'name': 'A Video',
    # 'status': 'accepted',
    # 'available': True,
    # 'tags': [],
    'user_id': doris_id,
    'kind': 'video',
    'data': {
      'site': 'youtube',
      'video_id': card_data['video_id'],
    },
    'unit_id': entity_ids_lookup[card_data['unit']],
    'require_ids': [],
  }
  raw_insert_cards(db_conn, [params])


for card_data in sample_data['cards']['page']:
  card_data['entity_id'] = uuid.uuid4()
  params = {
    'version_id': uuid.uuid4(),
    'created': datetime(2014, 1, 1, tzinfo=timezone.utc),
    'modified': datetime(2014, 1, 1, tzinfo=timezone.utc),
    'entity_id': card_data['entity_id'],
    'previous_id': None,
    # 'language': 'en',
    'name': card_data['name'],
    # 'status': 'accepted',
    # 'available': True,
    # 'tags': [],
    'user_id': doris_id,
    'kind': 'page',
    'data': {
      'body': card_data['body'],
    },
    'unit_id': entity_ids_lookup[card_data['unit']],
    'require_ids': [],
  }
  raw_insert_cards(db_conn, [params])


for card_data in sample_data['cards']['unscored_embed']:
  card_data['entity_id'] = uuid.uuid4()
  params = {
    'version_id': uuid.uuid4(),
    'created': datetime(2014, 1, 1, tzinfo=timezone.utc),
    'modified': datetime(2014, 1, 1, tzinfo=timezone.utc),
    'entity_id': card_data['entity_id'],
    'previous_id': None,
    # 'language': 'en',
    'name': 'An Example',
    # 'status': 'accepted',
    # 'available': True,
    # 'tags': [],
    'user_id': doris_id,
    'kind': 'unscored_embed',
    'data': {
      'url': card_data['url'],
    },
    'unit_id': entity_ids_lookup[card_data['unit']],
    'require_ids': [],
  }
  raw_insert_cards(db_conn, [params])


for card_data in sample_data['cards']['choice']:
  card_data['entity_id'] = uuid.uuid4()
  params = {
    'id': uuid.uuid4(),
    'version_id': uuid.uuid4(),
    'created': datetime(2014, 1, 1, tzinfo=timezone.utc),
    'modified': datetime(2014, 1, 1, tzinfo=timezone.utc),
    'entity_id': card_data['entity_id'],
    'previous_id': None,
    # 'language': 'en',
    'name': card_data['body'],
    # 'status': 'accepted',
    # 'available': True,
    # 'tags': [],
    'user_id': doris_id,
    'kind': 'choice',
    'data': {
      'body': card_data['body'],
      'options': [{
        'id': convert_uuid_to_slug(uuid.uuid4()),
        'correct': opt['correct'] == 'Y',
        'value': opt['value'],
        'feedback': opt['feedback'],
      } for opt in card_data['options']],
      'order': 'random',
      'max_options_to_show': 4,
    },
    'unit_id': entity_ids_lookup[card_data['unit']],
    'require_ids': [],
  }
  raw_insert_cards(db_conn, [params])


for sample_id, subject_data in sample_data['subjects'].items():
  if sample_id in entity_ids_lookup:
    subject_data['entity_id'] = entity_ids_lookup[sample_id]
  else:
    subject_data['entity_id'] = entity_ids_lookup[sample_id] = uuid.uuid4()

  u_members = []
  for member in subject_data['members']:
    if member['id'] not in entity_ids_lookup:
      entity_ids_lookup[member['id']] = uuid.uuid4()
    u_members.append({
      'id': convert_uuid_to_slug(entity_ids_lookup[member['id']]),
      'kind': member['kind'],
    })
  subject_data['members'] = u_members

  params = {
    'version_id': uuid.uuid4(),
    'created': datetime(2014, 1, 1, tzinfo=timezone.utc),
    'modified': datetime(2014, 1, 1, tzinfo=timezone.utc),
    'entity_id': subject_data['entity_id'],
    'previous_id': None,
    # 'language': 'en',
    'name': subject_data['name'],
    # 'status': 'accepted',
    # 'available': True,
    # 'tags': [],
    'user_id': doris_id,
    'body': subject_data['body'],
    'members': subject_data['members'],
  }
  raw_insert_subjects(db_conn, [params])


for sample_id, unit_data in sample_data['units'].items():
  topic_id = uuid.uuid4()
  proposal_id = uuid.uuid4()
  params = {
    'id': topic_id,
    'created': datetime(2014, 1, 1, tzinfo=timezone.utc),
    'modified': datetime(2014, 1, 1, tzinfo=timezone.utc),
    'user_id': doris_id,
    'name': '%s is fun' % unit_data['name'],
    'entity_id': unit_data['entity_id'],
    'entity_kind': 'unit',
  }
  raw_insert_topics(db_conn, [params])

  posts = [{
    'id': uuid.uuid4(),
    'created': datetime(2014, 1, 1, tzinfo=timezone.utc),
    'modified': datetime(2014, 1, 1, tzinfo=timezone.utc),
    'user_id': doris_id,
    'topic_id': topic_id,
    'body': '%s is such learning funness. ' % unit_data['name'] +
            'I dream about it all day long. ' +
            'What could be better?',
    'kind': 'post',
    'replies_to_id': None,
    'response': None,
  }, {
    'id': proposal_id,
    'created': datetime(2014, 1, 1, tzinfo=timezone.utc),
    'modified': datetime(2014, 1, 1, tzinfo=timezone.utc),
    'user_id': doris_id,
    'topic_id': topic_id,
    'body': 'I think we should do something to %s.' % unit_data['name'],
    'kind': 'proposal',
    'replies_to_id': None,
    'entity_versions': [{
      'id': convert_uuid_to_slug(unit_data['version_id']),
      'kind': 'unit',
    }],
    'name': 'Lets change %s' % unit_data['name'],
    'response': None,
  }, {
    'id': uuid.uuid4(),
    'created': datetime(2014, 1, 2, tzinfo=timezone.utc),
    'modified': datetime(2014, 1, 2, tzinfo=timezone.utc),
    'user_id': doris_id,
    'topic_id': topic_id,
    'body': 'I agree.',
    'kind': 'vote',
    'replies_to_id': proposal_id,
    'response': True,
  }]
  raw_insert_posts(db_conn, posts)

  params = {
    'id': uuid.uuid4(),
    'created': datetime(2014, 1, 1, tzinfo=timezone.utc),
    'modified': datetime(2014, 1, 1, tzinfo=timezone.utc),
    'user_id': doris_id,
    'entity_id': unit_data['entity_id'],
    'entity_kind': 'unit',
  }
  raw_insert_follows(db_conn, [params])

  params = {
    'id': uuid.uuid4(),
    'created': datetime(2014, 1, 1, tzinfo=timezone.utc),
    'modified': datetime(2014, 1, 1, tzinfo=timezone.utc),
    'user_id': doris_id,
    'kind': 'create_topic',
    'data': {
      'user_name': 'Eileen',
      'topic_name': '%s is fun' % unit_data['name'],
      'entity_kind': 'unit',
      'entity_name': unit_data['name'],
    },
    'read': False,
    'tags': [],
  }
  raw_insert_notices(db_conn, [params])

"""
TODO

r.table('users_subjects').insert({
  'id': 'doris-subjects',
  'created': datetime(2014, 1, 1, tzinfo=timezone.utc),
  'modified': datetime(2014, 1, 1, tzinfo=timezone.utc),
  'user_id': 'doris',
  'subject_ids': [
    sample_id
    for sample_id, subject_data in sample_data['subjects'].items()
  ],
}).run(db_conn)

"""

close_db_connection(db_conn)

es_populate()
