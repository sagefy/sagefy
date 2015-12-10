import rethinkdb as r
import framework.database as database
from framework.database import setup_db, make_db_connection, \
    close_db_connection
from framework.elasticsearch import es
from passlib.hash import bcrypt
from modules.sequencer.params import precision
from modules.util import json_prep, pick
from models.user import get_avatar
from sys import argv

setup_db()
make_db_connection()

for kind in (
    'users',
    'units',
    'units_parameters',
    'cards',
    'cards_parameters',
    'sets',
    'sets_parameters',
    'topics',
    'posts',
    'follows',
    'notices',
    'users_sets',
    'responses',
):
    (database.db.table(kind)
        .delete()
        .run(database.db_conn))

es.indices.delete(index='entity', ignore=[400, 404])

(database.db.table('users')
    .insert([{
        'id': 'doris',
        'created': r.time(2014, 1, 1, 'Z'),
        'modified': r.time(2014, 1, 1, 'Z'),
        'name': 'doris',
        'email': 'doris@example.com',
        'password': bcrypt.encrypt('example1'),
        'settings': {
            'email_frequency': 'daily',
            'view_sets': 'public',
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
            'view_sets': 'public',
            'view_follows': 'public',
        }
    }])
    .run(database.db_conn))

users = database.db.table('users').run(database.db_conn)
for user in users:
    data = pick(json_prep(user), ('id', 'name'))
    data['avatar'] = get_avatar(user['email'])
    es.index(
        index='entity',
        doc_type='user',
        body=data,
        id=user['id'],
    )

(database.db.table('units')
    .insert([{
        'id': 'plus-1',
        'created': r.time(2014, 1, 1, 'Z'),
        'modified': r.time(2014, 1, 1, 'Z'),
        'entity_id': 'plus',
        'previous_id': None,
        'language': 'en',
        'name': 'Adding two number together.',
        'status': 'accepted',
        'available': True,
        'tags': ['math'],
        'body': 'The joy and pleasure of adding numbers.',
        'require_ids': [],
    }, {
        'id': 'plus-2',
        'created': r.time(2014, 2, 1, 'Z'),
        'modified': r.time(2014, 2, 1, 'Z'),
        'entity_id': 'plus',
        'previous_id': 'plus-1',
        'language': 'en',
        'name': 'Adding two number together is fun.',
        'status': 'accepted',
        'available': True,
        'tags': ['math'],
        'body': 'The joy and pleasure of adding numbers.',
        'require_ids': [],
    }, {
        'id': 'plus-3',
        'created': r.time(2014, 2, 2, 'Z'),
        'modified': r.time(2014, 2, 2, 'Z'),
        'entity_id': 'plus',
        'previous_id': 'plus-1',
        'language': 'en',
        'name': 'Adding two number together grrr.',
        'status': 'declined',
        'available': True,
        'tags': ['math'],
        'body': 'The joy and pleasure of adding numbers.',
        'require_ids': [],
    }, {
        'id': 'minus-1',
        'created': r.time(2014, 1, 1, 'Z'),
        'modified': r.time(2014, 1, 1, 'Z'),
        'entity_id': 'minus',
        'previous_id': None,
        'language': 'en',
        'name': 'Subtracting two numbers.',
        'status': 'accepted',
        'available': True,
        'tags': ['math'],
        'body': 'The joy and pleasure of subtracting numbers.',
        'require_ids': ['plus'],
    }, {
        'id': 'minus-2',
        'created': r.time(2014, 2, 1, 'Z'),
        'modified': r.time(2014, 2, 1, 'Z'),
        'entity_id': 'minus',
        'previous_id': 'minus-1',
        'language': 'en',
        'name': 'Subtracting two numberz is unicorn.',
        'status': 'pending',
        'available': True,
        'tags': ['math'],
        'body': 'The joy and pleasure of subtracting numbers.',
        'require_ids': ['plus'],
    }, {
        'id': 'times-1',
        'created': r.time(2014, 1, 1, 'Z'),
        'modified': r.time(2014, 1, 1, 'Z'),
        'entity_id': 'times',
        'previous_id': None,
        'language': 'en',
        'name': 'Multiplying two numbers.',
        'status': 'accepted',
        'available': True,
        'tags': ['math'],
        'body': 'The joy and pleasure of multiplying numbers.',
        'require_ids': ['plus'],
    }, {
        'id': 'slash-1',
        'created': r.time(2014, 1, 1, 'Z'),
        'modified': r.time(2014, 1, 1, 'Z'),
        'entity_id': 'slash',
        'previous_id': None,
        'language': 'en',
        'name': 'Dividing two numbers.',
        'status': 'accepted',
        'available': True,
        'tags': ['math'],
        'body': 'The joy and pleasure of dividing numbers.',
        'require_ids': ['plus', 'minus', 'times'],
    }, {
        'id': 'slash-2',
        'created': r.time(2014, 2, 1, 'Z'),
        'modified': r.time(2014, 2, 1, 'Z'),
        'entity_id': 'slash',
        'previous_id': 'slash-1',
        'language': 'en',
        'name': 'Dividing two numberz.',
        'status': 'blocked',
        'available': True,
        'tags': ['math'],
        'body': 'The joy and pleasure of dividing numbers.',
        'require_ids': ['minus', 'times'],
    }])
    .run(database.db_conn))

units = (database.db.table('units')
                 .filter(r.row['id'] in (
                     'plus-2', 'minus-1', 'times-1', 'slash-1'
                 )).run(database.db_conn))
for unit in units:
    es.index(
        index='entity',
        doc_type='unit',
        body=json_prep(unit),
        id=unit['entity_id'],
    )

(database.db.table('units_parameters')
    .insert([{
        'id': 'plus-params',
        'created': r.time(2014, 2, 1, 'Z'),
        'modified': r.time(2014, 2, 1, 'Z'),
        'entity_id': 'plus',
    }])
    .run(database.db_conn))


# TODO@ create at least one video and one choice per unit
(database.db.table('cards')
    .insert([{
        'id': 'plus-video-a-1',
        'created': r.time(2014, 1, 1, 'Z'),
        'modifed': r.time(2014, 1, 1, 'Z'),
        'entity_id': 'plus-video-a',
        'previous_id': None,
        'language': 'en',
        'name': 'How to add by...',
        'status': 'accepted',
        'available': True,
        'tags': ['video'],
        'unit_id': 'plus',
        'require_ids': [],
        'kind': 'video',
        'site': 'youtube',
        'video_id': 'PS5p9caXS4U'
    }, {
        'id': 'plus-choice-a-1',
        'created': r.time(2014, 1, 1, 'Z'),
        'modifed': r.time(2014, 1, 1, 'Z'),
        'entity_id': 'plus-choice-a',
        'previous_id': None,
        'language': 'en',
        'name': 'Let\'s add 2 + 2',
        'status': 'accepted',
        'available': True,
        'tags': [],
        'unit_id': 'plus',
        'require_ids': [],
        'kind': 'choice',
        'body': 'What is 2 + 2?',
        'options': [{
            'value': '2',
            'correct': False,
            'feedback': 'There are two numbers.',
        }, {
            'value': '0',
            'correct': False,
            'feedback': 'We are not subtracting.',
        }, {
            'value': '4',
            'correct': True,
            'feedback': 'Yes, 2 + 2 = 4.',
        }],
        'order': 'random',
        'max_options_to_show': 4,
    }, {
        'id': 'plus-choice-b-1',
        'created': r.time(2014, 1, 1, 'Z'),
        'modifed': r.time(2014, 1, 1, 'Z'),
        'entity_id': 'plus-choice-b',
        'previous_id': None,
        'language': 'en',
        'name': 'Let\'s add 3 + 1',
        'status': 'accepted',
        'available': True,
        'tags': [],
        'unit_id': 'plus',
        'require_ids': [],
        'kind': 'choice',
        'body': 'What is 3 + 1?',
        'options': [{
            'value': '3',
            'correct': False,
            'feedback': 'There are two numbers.',
        }, {
            'value': '1',
            'correct': False,
            'feedback': 'There are two numbers.',
        }, {
            'value': '4',
            'correct': True,
            'feedback': 'Yes, 3 + 1 = 4.',
        }],
        'order': 'random',
        'max_options_to_show': 4,
    }])
    .run(database.db_conn))

cards = database.db.table('cards').run(database.db_conn)
for card in cards:
    es.index(
        index='entity',
        doc_type='card',
        body=json_prep(card),
        id=card['entity_id'],
    )

(database.db.table('cards_parameters')
    .insert([{
        'id': 'plus-video-a-params',
        'created': r.time(2014, 1, 1, 'Z'),
        'modifed': r.time(2014, 1, 1, 'Z'),
        'entity_id': 'plus-video-a',
    }, {
        'id': 'plus-choice-a-params',
        'created': r.time(2014, 1, 1, 'Z'),
        'modifed': r.time(2014, 1, 1, 'Z'),
        'entity_id': 'plus-choice-a',
        'guess_distribution': {
            str(h): 1 - (0.5 - h) ** 2
            for h in [h / precision for h in range(1, precision)]
        },
        'slip_distribution': {
            str(h): 1 - (0.25 - h) ** 2
            for h in [h / precision for h in range(1, precision)]
        }
    }, {
        'id': 'plus-choice-b-params',
        'created': r.time(2014, 1, 1, 'Z'),
        'modifed': r.time(2014, 1, 1, 'Z'),
        'entity_id': 'plus-choice-b',
        'guess_distribution': {
            str(h): 1 - (0.5 - h) ** 2
            for h in [h / precision for h in range(1, precision)]
        },
        'slip_distribution': {
            str(h): 1 - (0.25 - h) ** 2
            for h in [h / precision for h in range(1, precision)]
        }
    }])
    .run(database.db_conn))

(database.db.table('sets')
    .insert([{
        'id': 'basic-math-1',
        'created': r.time(2014, 1, 1, 'Z'),
        'modified': r.time(2014, 1, 1, 'Z'),
        'entity_id': 'basic-math',
        'previous_id': None,
        'language': 'en',
        'name': 'Basic Math',
        'status': 'accepted',
        'available': True,
        'tags': ['basic'],
        'body': 'Learn some adding, subtracting, multiplying, and dividing.',
        'members': [{
            'id': 'plus',
            'kind': 'unit',
        }, {
            'id': 'minus',
            'kind': 'unit',
        }, {
            'id': 'times',
            'kind': 'unit',
        }, {
            'id': 'slash',
            'kind': 'unit',
        }]
    }])
    .run(database.db_conn))

sets = database.db.table('sets').run(database.db_conn)
for set_ in sets:
    es.index(
        index='entity',
        doc_type='set',
        body=json_prep(set_),
        id=set_['entity_id'],
    )

(database.db.table('sets_parameters')
    .insert([{
        'id': 'basic-math-params',
        'created': r.time(2014, 1, 1, 'Z'),
        'modified': r.time(2014, 1, 1, 'Z'),
        'entity_id': 'basic-math',
    }])
    .run(database.db_conn))

(database.db.table('topics')
    .insert([{
        'id': 'basic-math-posts',
        'created': r.time(2014, 1, 1, 'Z'),
        'modified': r.time(2014, 1, 1, 'Z'),
        'user_id': 'doris',
        'name': 'Basic math is fun',
        'entity': {
            'id': 'basic-math',
            'kind': 'set',
        }
    }, {
        'id': 'plus-changes',
        'created': r.time(2014, 1, 1, 'Z'),
        'modified': r.time(2014, 1, 1, 'Z'),
        'user_id': 'eileen',
        'name': 'Lets do some changes with plus',
        'entity': {
            'id': 'plus',
            'kind': 'unit',
        }
    }, {
        'id': 'minus-changes',
        'created': r.time(2014, 1, 1, 'Z'),
        'modified': r.time(2014, 1, 1, 'Z'),
        'user_id': 'eileen',
        'name': 'Lets make some changes with minus',
        'entity': {
            'id': 'minus',
            'kind': 'unit',
        }
    }, {
        'id': 'slash-changes',
        'created': r.time(2014, 1, 1, 'Z'),
        'modified': r.time(2014, 1, 1, 'Z'),
        'user_id': 'eileen',
        'name': 'Lets block some changes with slash',
        'entity': {
            'id': 'slash',
            'kind': 'unit',
        }
    }])
    .run(database.db_conn))

topics = database.db.table('topics').run(database.db_conn)
for topic in topics:
    es.index(
        index='entity',
        doc_type='topic',
        body=json_prep(topic),
        id=topic['id'],
    )

(database.db.table('posts')
    .insert([{
        'id': 'basic-math-fun-1',
        'created': r.time(2014, 1, 1, 'Z'),
        'modified': r.time(2014, 1, 1, 'Z'),
        'user_id': 'doris',
        'topic_id': 'basic-math-posts',
        'body': 'OMG basic math is such learning funness. ' +
                'I dream about math all day long. ' +
                'What could be better?',
        'kind': 'post',
        'replies_to_id': None,
    }, {
        'id': 'basic-math-fun-2',
        'created': r.time(2014, 1, 2, 'Z'),
        'modified': r.time(2014, 1, 2, 'Z'),
        'user_id': 'eileen',
        'topic_id': 'basic-math-posts',
        'body': 'I suppose.',
        'kind': 'post',
        'replies_to_id': 'basic-math-fun-1',
    }, {
        'id': 'basic-math-fun-3',
        'created': r.time(2014, 1, 3, 'Z'),
        'modified': r.time(2014, 1, 3, 'Z'),
        'user_id': 'doris',
        'topic_id': 'basic-math-posts',
        'body': 'I really love math.',
        'kind': 'post',
        'replies_to_id': None,
    }, {
        'id': 'minus-proposal-pending',
        'created': r.time(2014, 1, 1, 'Z'),
        'modified': r.time(2014, 1, 1, 'Z'),
        'user_id': 'doris',
        'topic_id': 'minus-changes',
        'body': 'I think we should make subtracting more fun.',
        'kind': 'proposal',
        'replies_to_id': None,
        'entity_version': {
            'id': 'minus-2',
            'kind': 'unit',
        },
        'name': 'Subtracting fun.',
    }, {
        'id': 'plus-proposal-accepted',
        'created': r.time(2014, 1, 1, 'Z'),
        'modified': r.time(2014, 1, 2, 'Z'),
        'user_id': 'eileen',
        'topic_id': 'plus-changes',
        'body': 'Yeah, totally! Lets make adding more fun.',
        'kind': 'proposal',
        'replies_to_id': None,
        'entity_version': {
            'id': 'plus-2',
            'kind': 'unit',
        },
        'name': 'Adding funness.',
    }, {
        'id': 'plus-vote-accept',
        'created': r.time(2014, 1, 2, 'Z'),
        'modified': r.time(2014, 1, 2, 'Z'),
        'user_id': 'doris',
        'topic_id': 'plus-changes',
        'body': 'I agree.',
        'kind': 'vote',
        'replies_to_id': 'plus-proposal-accepted',
        'response': False,
    }, {
        'id': 'plus-proposal-declined',
        'created': r.time(2014, 1, 2, 'Z'),
        'modified': r.time(2014, 1, 3, 'Z'),
        'user_id': 'doris',
        'topic_id': 'plus-changes',
        'body': 'Let\'s make it even more fun!',
        'kind': 'proposal',
        'replies_to_id': None,
        'entity_version': {
            'id': 'plus-3',
            'kind': 'unit',
        },
        'name': 'Funner!',
    }, {
        'id': 'plus-vote-block',
        'created': r.time(2014, 1, 3, 'Z'),
        'modified': r.time(2014, 1, 3, 'Z'),
        'user_id': 'eileen',
        'topic_id': 'plus-changes',
        'body': 'Boo!',
        'kind': 'vote',
        'replies_to_id': 'plus-proposal-declined',
        'response': False,
    }, {
        'id': 'slash-proposal-blocked',
        'created': r.time(2014, 1, 1, 'Z'),
        'modified': r.time(2014, 1, 2, 'Z'),
        'user_id': 'doris',
        'topic_id': 'slash-changes',
        'body': 'More serious!',
        'kind': 'proposal',
        'replies_to_id': None,
        'entity_version': {
            'id': 'slash-2',
            'kind': 'unit',
        },
        'name': 'Let\'s make dividing more serious.',
    }, {
        'id': 'slash-vote-block',
        'created': r.time(2014, 1, 2, 'Z'),
        'modified': r.time(2014, 1, 2, 'Z'),
        'user_id': 'eileen',
        'topic_id': 'slash-changes',
        'body': 'I hate this.',
        'kind': 'vote',
        'replies_to_id': 'slash-proposal-blocked',
        'response': False,
    }])
    .run(database.db_conn))

posts = database.db.table('posts').run(database.db_conn)
for post in posts:
    data = json_prep(post)
    topic = (database.db.table('topics')
                     .get(data['topic_id'])
                     .run(database.db_conn))
    user = (database.db.table('users')
                    .get(data['user_id'])
                    .run(database.db_conn))
    data['topic'] = json_prep(topic)
    data['user'] = json_prep(user)
    es.index(
        index='entity',
        doc_type='post',
        body=data,
        id=post['id'],
    )

(database.db.table('follows')
    .insert([{
        'id': 'doris-follows-basic-math',
        'created': r.time(2014, 1, 1, 'Z'),
        'modified': r.time(2014, 1, 1, 'Z'),
        'user_id': 'doris',
        'entity': {
            'id': 'basic-math',
            'kind': 'set',
        }
    }, {
        'id': 'doris-follows-plus',
        'created': r.time(2014, 1, 1, 'Z'),
        'modified': r.time(2014, 1, 1, 'Z'),
        'user_id': 'doris',
        'entity': {
            'id': 'plus',
            'kind': 'unit',
        }
    }, {
        'id': 'doris-follows-minus',
        'created': r.time(2014, 1, 1, 'Z'),
        'modified': r.time(2014, 1, 1, 'Z'),
        'user_id': 'doris',
        'entity': {
            'id': 'minus',
            'kind': 'unit',
        }
    }, {
        'id': 'doris-follows-slash',
        'created': r.time(2014, 1, 1, 'Z'),
        'modified': r.time(2014, 1, 1, 'Z'),
        'user_id': 'doris',
        'entity': {
            'id': 'slash',
            'kind': 'unit',
        }
    }])
    .run(database.db_conn))

(database.db.table('notices')
    .insert([{
        'id': 'doris-new-topic-basic-math',
        'created': r.time(2014, 1, 1, 'Z'),
        'modified': r.time(2014, 1, 1, 'Z'),
        'user_id': 'doris',
        'kind': 'create_topic',
        'data': {
            'user_name': 'Eileen',
            'topic_name': 'Basic math is fun.',
            'entity_kind': 'set',
            'entity_name': 'Basic Math',
        },
        'read': False,
        'tags': [],
    }, {
        'id': 'doris-create-proposal-minus',
        'created': r.time(2014, 1, 2, 'Z'),
        'modified': r.time(2014, 1, 2, 'Z'),
        'user_id': 'doris',
        'kind': 'create_proposal',
        'data': {
            'user_name': 'Eileen',
            'proposal_name': 'To subtract or not to subtract.',
            'entity_kind': 'unit',
            'entity_name': 'Subtracting two numbers',
        },
        'read': False,
        'tags': [],
    }, {
        'id': 'doris-block-proposal-slash',
        'created': r.time(2014, 1, 3, 'Z'),
        'modified': r.time(2014, 1, 3, 'Z'),
        'user_id': 'doris',
        'kind': 'block_proposal',
        'data': {
            'user_name': 'Eileen',
            'proposal_name': 'Division is stupid.',
            'entity_kind': 'unit',
            'entity_name': 'Dividing two numbers',
        },
        'read': False,
        'tags': [],
    }, {
        'id': 'doris-accept-proposal-plus',
        'created': r.time(2014, 1, 2, 'Z'),
        'modified': r.time(2014, 1, 2, 'Z'),
        'user_id': 'doris',
        'kind': 'accept_proposal',
        'data': {
            'user_name': 'Eileen',
            'proposal_name': 'Adding is fun.',
            'entity_kind': 'unit',
            'entity_name': 'Adding two numbers',
        },
        'read': False,
        'tags': [],
    }])
    .run(database.db_conn))

(database.db.table('users_sets')
    .insert([{
        'id': 'doris-sets',
        'created': r.time(2014, 1, 1, 'Z'),
        'modified': r.time(2014, 1, 1, 'Z'),
        'user_id': 'doris',
        'set_ids': ['basic-math'],
    }])
    .run(database.db_conn))

# id, created, modified
# user_id, card_id, unit_id, response, score, learned
if len(argv) > 1 and argv[1] == 'learn_mode':
    (database.db.table('responses')
        .insert([{
            'id': 'response1',
            'created': r.now(),
            'modified': r.now(),
            'user_id': 'doris',
            'card_id': 'plus-choice-a',
            'unit_id': 'plus',
            'response': 1,
            'score': 1,
            'learned': 1,
        }, {
            'id': 'response2',
            'created': r.now(),
            'modified': r.now(),
            'user_id': 'doris',
            'card_id': 'minus-choice-a',
            'unit_id': 'minus',
            'response': 1,
            'score': 1,
            'learned': 0.5,
        }, {
            'id': 'response3',
            'created': r.now(),
            'modified': r.now(),
            'user_id': 'doris',
            'card_id': 'times-choice-a',
            'unit_id': 'times',
            'response': 1,
            'score': 1,
            'learned': 1,
        }, {
            'id': 'response4',
            'created': r.now(),
            'modified': r.now(),
            'user_id': 'doris',
            'card_id': 'slash-choice-a',
            'unit_id': 'slash',
            'response': 1,
            'score': 1,
            'learned': 0.5
        }])
        .run(database.db_conn))

close_db_connection()
