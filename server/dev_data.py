import rethinkdb as r
from framework.database import setup_db, make_db_connection, \
    close_db_connection
from framework.elasticsearch import es
from passlib.hash import bcrypt
from modules.sequencer.params import precision
from modules.util import uniqid
from config import config
from es_populate import es_populate
import yaml
import os
from framework.redis import redis


if not config['debug']:
    raise Exception('You must be in debug mode to wipe the DB.')

setup_db()
db_conn = make_db_connection()

for kind in (
    'users',
    'units',
    'cards',
    'cards_parameters',
    'subjects',
    'topics',
    'posts',
    'follows',
    'notices',
    'users_subjects',
    'responses',
):
    (r.table(kind)
      .delete()
      .run(db_conn))

es.indices.delete(index='entity', ignore=[400, 404])

redis.flushall()

dirname = os.path.realpath(__file__).replace('/server/dev_data.py', '')
stream = open(
    '%s/server/intro_electronic_music_example_collection.yaml' % (dirname,),
    'r'
)
sample_data = yaml.load(stream)
stream.close()

(r.table('users')
    .insert([{
        'id': 'doris',
        'created': r.time(2014, 1, 1, 'Z'),
        'modified': r.time(2014, 1, 1, 'Z'),
        'name': 'doris',
        'email': 'doris@example.com',
        'password': bcrypt.encrypt('example1'),
        'settings': {
            'email_frequency': 'daily',
            'view_subjects': 'public',
            'view_follows': 'public',
        }
    }, {
        'id': 'eileen',
        'created': r.time(2014, 1, 1, 'Z'),
        'modified': r.time(2014, 1, 1, 'Z'),
        'name': 'eileen',
        'email': 'eileen@example.com',
        'password': bcrypt.encrypt('example1'),
        'settings': {
            'email_frequency': 'daily',
            'view_subjects': 'public',
            'view_follows': 'public',
        }
    }])
    .run(db_conn))


for sample_id, unit_data in sample_data['units'].items():
    unit_data['entity_id'] = sample_id
    unit_data['version_id'] = uniqid()
    r.table('units').insert({
        'id': unit_data['version_id'],
        'created': r.time(2014, 1, 1, 'Z'),
        'modified': r.time(2014, 1, 1, 'Z'),
        'entity_id': unit_data['entity_id'],
        'previous_id': None,
        'language': 'en',
        'status': 'accepted',
        'available': True,
        'tags': [],
        'name': unit_data['name'],
        'body': unit_data['body'],
        'require_ids': unit_data['requires'],
    }).run(db_conn)


for card_data in sample_data['cards']['video']:
    card_data['entity_id'] = uniqid()
    r.table('cards').insert({
        'id': uniqid(),
        'created': r.time(2014, 1, 1, 'Z'),
        'modified': r.time(2014, 1, 1, 'Z'),
        'entity_id': card_data['entity_id'],
        'previous_id': None,
        'language': 'en',
        'name': 'A Video',
        'status': 'accepted',
        'available': True,
        'tags': [],
        'kind': 'video',
        'site': 'youtube',
        'video_id': card_data['video_id'],
        'unit_id': card_data['unit'],
        'require_ids': [],
    }).run(db_conn)
    r.table('cards_parameters').insert({
        'id': uniqid(),
        'created': r.time(2014, 1, 1, 'Z'),
        'modified': r.time(2014, 1, 1, 'Z'),
        'entity_id': card_data['entity_id'],
    }).run(db_conn)


for card_data in sample_data['cards']['choice']:
    card_data['entity_id'] = uniqid()
    r.table('cards').insert({
        'id': uniqid(),
        'created': r.time(2014, 1, 1, 'Z'),
        'modified': r.time(2014, 1, 1, 'Z'),
        'entity_id': card_data['entity_id'],
        'previous_id': None,
        'language': 'en',
        'name': card_data['body'],
        'status': 'accepted',
        'available': True,
        'tags': [],
        'kind': 'choice',
        'body': card_data['body'],
        'options': [
            {
                'correct': opt['correct'] == 'Y',
                'value': opt['value'],
                'feedback': opt['feedback'],
            } for opt in card_data['options']
        ],
        'order': 'random',
        'max_options_to_show': 4,
        'unit_id': card_data['unit'],
        'require_ids': [],
    }).run(db_conn)
    r.table('cards_parameters').insert({
        'id': uniqid(),
        'created': r.time(2014, 1, 1, 'Z'),
        'modified': r.time(2014, 1, 1, 'Z'),
        'entity_id': card_data['entity_id'],
        'guess_distribution': {
            str(h): 1 - (0.5 - h) ** 2
            for h in [h / precision for h in range(1, precision)]
        },
        'slip_distribution': {
            str(h): 1 - (0.25 - h) ** 2
            for h in [h / precision for h in range(1, precision)]
        }
    }).run(db_conn)


for sample_id, subject_data in sample_data['subjects'].items():
    subject_data['entity_id'] = sample_id
    r.table('subjects').insert({
        'id': uniqid(),
        'created': r.time(2014, 1, 1, 'Z'),
        'modified': r.time(2014, 1, 1, 'Z'),
        'entity_id': subject_data['entity_id'],
        'previous_id': None,
        'language': 'en',
        'name': subject_data['name'],
        'status': 'accepted',
        'available': True,
        'tags': [],
        'body': subject_data['body'],
        'members': subject_data['members'],
    }).run(db_conn)


for sample_id, unit_data in sample_data['units'].items():
    topic_id = uniqid()
    proposal_id = uniqid()
    r.table('topics').insert({
        'id': topic_id,
        'created': r.time(2014, 1, 1, 'Z'),
        'modified': r.time(2014, 1, 1, 'Z'),
        'user_id': 'doris',
        'name': '%s is fun' % unit_data['name'],
        'entity': {
            'id': unit_data['entity_id'],
            'kind': 'unit',
        }
    }).run(db_conn)
    r.table('posts').insert([{
        'id': uniqid(),
        'created': r.time(2014, 1, 1, 'Z'),
        'modified': r.time(2014, 1, 1, 'Z'),
        'user_id': 'doris',
        'topic_id': topic_id,
        'body': '%s is such learning funness. ' % unit_data['name'] +
                'I dream about it all day long. ' +
                'What could be better?',
        'kind': 'post',
        'replies_to_id': None,
    }, {
        'id': proposal_id,
        'created': r.time(2014, 1, 1, 'Z'),
        'modified': r.time(2014, 1, 1, 'Z'),
        'user_id': 'doris',
        'topic_id': topic_id,
        'body': 'I think we should do something to %s.' % unit_data['name'],
        'kind': 'proposal',
        'replies_to_id': None,
        'entity_versions': [{
            'id': unit_data['version_id'],
            'kind': 'unit',
        }],
        'name': 'Lets change %s' % unit_data['name'],
    }, {
        'id': uniqid(),
        'created': r.time(2014, 1, 2, 'Z'),
        'modified': r.time(2014, 1, 2, 'Z'),
        'user_id': 'doris',
        'topic_id': topic_id,
        'body': 'I agree.',
        'kind': 'vote',
        'replies_to_id': proposal_id,
        'response': True,
    }]).run(db_conn)
    r.table('follows').insert({
        'id': uniqid(),
        'created': r.time(2014, 1, 1, 'Z'),
        'modified': r.time(2014, 1, 1, 'Z'),
        'user_id': 'doris',
        'entity': {
            'id': unit_data['entity_id'],
            'kind': 'unit',
        }
    }).run(db_conn)
    r.table('notices').insert({
        'id': uniqid(),
        'created': r.time(2014, 1, 1, 'Z'),
        'modified': r.time(2014, 1, 1, 'Z'),
        'user_id': 'doris',
        'kind': 'create_topic',
        'data': {
            'user_name': 'Eileen',
            'topic_name': '%s is fun' % unit_data['name'],
            'entity_kind': 'unit',
            'entity_name': unit_data['name'],
        },
        'read': False,
        'tags': [],
    }).run(db_conn)


r.table('users_subjects').insert({
    'id': 'doris-subjects',
    'created': r.time(2014, 1, 1, 'Z'),
    'modified': r.time(2014, 1, 1, 'Z'),
    'user_id': 'doris',
    'subject_ids': [
        sample_id
        for sample_id, subject_data in sample_data['subjects'].items()
    ],
}).run(db_conn)

close_db_connection(db_conn)

es_populate()
