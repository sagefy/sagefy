import psycopg2
import psycopg2.extras
from framework.database import make_db_connection, \
    close_db_connection
from framework.elasticsearch import es
from passlib.hash import bcrypt
from modules.sequencer.params import precision
from config import config
from es_populate import es_populate
import yaml
import os
from framework.redis import redis
from datetime import datetime, timezone
import uuid


if not config['debug']:
    raise Exception('You must be in debug mode to wipe the DB.')

psycopg2.extras.register_uuid()
db_conn = make_db_connection()

for tablename in reversed((
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
)):
    cur = db_conn.cursor()
    with cur:
        cur.execute("DELETE FROM {tablename};".format(tablename=tablename))
        db_conn.commit()

es.indices.delete(index='entity', ignore=[400, 404])

redis.flushall()

dirname = os.path.realpath(__file__).replace('/server/dev_data.py', '')
stream = open(
    '%s/server/intro_electronic_music_example_collection.yaml' % (dirname,),
    'r'
)
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
    'password': bcrypt.encrypt('example1'),
    'settings': psycopg2.extras.Json({
        'email_frequency': 'daily',
        'view_subjects': 'public',
        'view_follows': 'public',
    })
}, {
    'id': eileen_id,
    'created': datetime(2014, 1, 1, tzinfo=timezone.utc),
    'modified': datetime(2014, 1, 1, tzinfo=timezone.utc),
    'name': 'eileen',
    'email': 'eileen@example.com',
    'password': bcrypt.encrypt('example1'),
    'settings': psycopg2.extras.Json({
        'email_frequency': 'daily',
        'view_subjects': 'public',
        'view_follows': 'public',
    })
}]

for user in users:
    cur = db_conn.cursor()
    with cur:
        cur.execute("""
            INSERT INTO users
            (  id  ,   created  ,   modified  ,
               name  ,   email,   password  ,   settings)
            VALUES
            (%(id)s, %(created)s, %(modified)s,
             %(name)s, %(email)s, %(password)s, %(settings)s);
        """, user)
        db_conn.commit()


# We have to translate the sample IDs to UUIDs
entity_ids_lookup = {}

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

    cur = db_conn.cursor()
    # Dropping foreign key checks so the ordering doesn't matter.
    with cur:
        cur.execute("""
            BEGIN;
            ALTER TABLE units DISABLE TRIGGER ALL;
            INSERT INTO units_entity_id
            (  entity_id  )
            VALUES
            (%(entity_id)s);
            INSERT INTO units
            (  version_id  ,   created  ,   modified  ,
               entity_id  ,   previous_id  ,   language  ,   status  ,
               available  ,   tags  ,   name  ,   user_id  ,
               body  ,   require_ids  )
            VALUES
            (%(version_id)s, %(created)s, %(modified)s,
             %(entity_id)s, %(previous_id)s, %(language)s, %(status)s,
             %(available)s, %(tags)s, %(name)s, %(user_id)s,
             %(body)s, %(require_ids)s);
            ALTER TABLE units ENABLE TRIGGER ALL;
            COMMIT;
        """, {
            'version_id': unit_data['version_id'],
            'created': datetime(2014, 1, 1, tzinfo=timezone.utc),
            'modified': datetime(2014, 1, 1, tzinfo=timezone.utc),
            'entity_id': unit_data['entity_id'],
            'previous_id': None,
            'language': 'en',
            'status': 'accepted',
            'available': True,
            'tags': [],
            'name': unit_data['name'],
            'user_id': doris_id,
            'body': unit_data['body'],
            'require_ids': unit_data['require_ids'],
        })
        db_conn.commit()


for card_data in sample_data['cards']['video']:
    card_data['entity_id'] = uuid.uuid4()

    cur = db_conn.cursor()
    with cur:
        cur.execute("""
            INSERT INTO cards_entity_id
            (  entity_id  )
            VALUES
            (%(entity_id)s);
            INSERT INTO cards
            (  version_id  ,   created  ,   modified  ,
               entity_id  ,   previous_id  ,   language  ,   status  ,
               available  ,   tags  ,   name  ,   user_id  ,
               unit_id  ,   require_ids  ,   kind  ,   data  )
            VALUES
            (%(version_id)s, %(created)s, %(modified)s,
             %(entity_id)s, %(previous_id)s, %(language)s, %(status)s,
             %(available)s, %(tags)s, %(name)s, %(user_id)s,
             %(unit_id)s, %(require_ids)s, %(kind)s, %(data)s);
        """, {
            'version_id': uuid.uuid4(),
            'created': datetime(2014, 1, 1, tzinfo=timezone.utc),
            'modified': datetime(2014, 1, 1, tzinfo=timezone.utc),
            'entity_id': card_data['entity_id'],
            'previous_id': None,
            'language': 'en',
            'name': 'A Video',
            'status': 'accepted',
            'available': True,
            'tags': [],
            'user_id': doris_id,
            'kind': 'video',
            'data': psycopg2.extras.Json({
                'site': 'youtube',
                'video_id': card_data['video_id'],
            }),
            'unit_id': entity_ids_lookup[card_data['unit']],
            'require_ids': [],
        })
        db_conn.commit()


for card_data in sample_data['cards']['choice']:
    card_data['entity_id'] = uuid.uuid4()
    r.table('cards').insert({
        'id': uuid.uuid4(),
        'created': datetime(2014, 1, 1, tzinfo=timezone.utc),
        'modified': datetime(2014, 1, 1, tzinfo=timezone.utc),
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
        'id': uuid.uuid4(),
        'created': datetime(2014, 1, 1, tzinfo=timezone.utc),
        'modified': datetime(2014, 1, 1, tzinfo=timezone.utc),
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
    """

        cur = db_conn.cursor()
        with cur:
            cur.execute(""
                INSERT INTO cards_parameters
                (  id  ,   created  ,   modified  ,   entity_id  )
                VALUES
                (%(id)s, %(created)s, %(modified)s, %(entity_id)s);
            "", {
                'id': uuid.uuid4(),
                'created': datetime(2014, 1, 1, tzinfo=timezone.utc),
                'modified': datetime(2014, 1, 1, tzinfo=timezone.utc),
                'entity_id': card_data['entity_id'],
            })
            db_conn.commit()
    """

for sample_id, subject_data in sample_data['subjects'].items():
    subject_data['entity_id'] = sample_id
    r.table('subjects').insert({
        'id': uuid.uuid4(),
        'created': datetime(2014, 1, 1, tzinfo=timezone.utc),
        'modified': datetime(2014, 1, 1, tzinfo=timezone.utc),
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
    topic_id = uuid.uuid4()
    proposal_id = uuid.uuid4()
    r.table('topics').insert({
        'id': topic_id,
        'created': datetime(2014, 1, 1, tzinfo=timezone.utc),
        'modified': datetime(2014, 1, 1, tzinfo=timezone.utc),
        'user_id': 'doris',
        'name': '%s is fun' % unit_data['name'],
        'entity': {
            'id': unit_data['entity_id'],
            'kind': 'unit',
        }
    }).run(db_conn)
    r.table('posts').insert([{
        'id': uuid.uuid4(),
        'created': datetime(2014, 1, 1, tzinfo=timezone.utc),
        'modified': datetime(2014, 1, 1, tzinfo=timezone.utc),
        'user_id': 'doris',
        'topic_id': topic_id,
        'body': '%s is such learning funness. ' % unit_data['name'] +
                'I dream about it all day long. ' +
                'What could be better?',
        'kind': 'post',
        'replies_to_id': None,
    }, {
        'id': proposal_id,
        'created': datetime(2014, 1, 1, tzinfo=timezone.utc),
        'modified': datetime(2014, 1, 1, tzinfo=timezone.utc),
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
        'id': uuid.uuid4(),
        'created': datetime(2014, 1, 2, tzinfo=timezone.utc),
        'modified': datetime(2014, 1, 2, tzinfo=timezone.utc),
        'user_id': 'doris',
        'topic_id': topic_id,
        'body': 'I agree.',
        'kind': 'vote',
        'replies_to_id': proposal_id,
        'response': True,
    }]).run(db_conn)
    r.table('follows').insert({
        'id': uuid.uuid4(),
        'created': datetime(2014, 1, 1, tzinfo=timezone.utc),
        'modified': datetime(2014, 1, 1, tzinfo=timezone.utc),
        'user_id': 'doris',
        'entity': {
            'id': unit_data['entity_id'],
            'kind': 'unit',
        }
    }).run(db_conn)
    r.table('notices').insert({
        'id': uuid.uuid4(),
        'created': datetime(2014, 1, 1, tzinfo=timezone.utc),
        'modified': datetime(2014, 1, 1, tzinfo=timezone.utc),
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
    'created': datetime(2014, 1, 1, tzinfo=timezone.utc),
    'modified': datetime(2014, 1, 1, tzinfo=timezone.utc),
    'user_id': 'doris',
    'subject_ids': [
        sample_id
        for sample_id, subject_data in sample_data['subjects'].items()
    ],
}).run(db_conn)

close_db_connection(db_conn)

es_populate()
