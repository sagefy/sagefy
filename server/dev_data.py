import rethinkdb as r
import framework.database as database
from framework.database import setup_db, make_db_connection, \
    close_db_connection
from passlib.hash import bcrypt
from modules.sequencer.params import precision

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
    }])
    .run(database.db_conn))

# id, created, modified
# entity_id, previous_id, language, name, status, available, tags
# body, require_ids
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

# id, created, modified
# entity_id
(database.db.table('units_parameters')
    .insert([{
        'id': 'plus-params',
        'created': r.time(2014, 2, 1, 'Z'),
        'modified': r.time(2014, 2, 1, 'Z'),
        'entity_id': 'plus',
    }])
    .run(database.db_conn))

# id, created, modified
# entity_id, previous_id, language, name, status, available, tags
# unit_id, require_ids, kind
# video: site, video_id
# choice: body, options[value, correct, feedback], order:'random',
#         max_options_to_show:4
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

# id, created, modified
# entity_id, guess_distribution, slip_distribution
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
            h: 1 - (0.5 - h) ** 2
            for h in [h / precision for h in range(1, precision)]
        },
        'slip_distribution': {
            h: 1 - (0.25 - h) ** 2
            for h in [h / precision for h in range(1, precision)]
        }
    }, {
        'id': 'plus-choice-b-params',
        'created': r.time(2014, 1, 1, 'Z'),
        'modifed': r.time(2014, 1, 1, 'Z'),
        'entity_id': 'plus-choice-b',
        'guess_distribution': {
            h: 1 - (0.5 - h) ** 2
            for h in [h / precision for h in range(1, precision)]
        },
        'slip_distribution': {
            h: 1 - (0.25 - h) ** 2
            for h in [h / precision for h in range(1, precision)]
        }
    }])
    .run(database.db_conn))

# id, created, modified
# entity_id, previous_id, language, name, status, available, tags
# body, members#id, members#kind
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

# id, created, modified
# entity_id
(database.db.table('sets_parameters')
    .insert([{
        'id': 'basic-math-params',
        'created': r.time(2014, 1, 1, 'Z'),
        'modified': r.time(2014, 1, 1, 'Z'),
        'entity_id': 'basic-math',
    }])
    .run(database.db_conn))

# TODO
# id, created, modified
# user_id, name, entity.id, entity.kind
(database.db.table('topics')
    .insert([{
    }])
    .run(database.db_conn))

# TODO proposal .. vote .. flag
# id, created, modified
# post: user_id, topic_id, body, kind, replies_to_id
# proposal: entity_version.id, entity_version.kind, name
# flag: reason: irrelevant
# vote: body, replies_to_id, response
(database.db.table('posts')
    .insert([{
    }])
    .run(database.db_conn))

# id, created, modified
# user_id, entity.id, entity.kind
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

# id, created, modified
# user_id, kind, read, tags
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
        'user_id': 'eileen',
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
        'user_id': 'eileen',
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
        'user_id': 'eileen',
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

# id, created, modified
# user_id, set_ids
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
# (database.db.table('responses')
#     .insert([{
#     }])
#     .run(database.db_conn))

close_db_connection()
