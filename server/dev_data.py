import rethinkdb as r
from framework.database import setup_db, make_db_connection, \
    close_db_connection
from framework.elasticsearch import es
from passlib.hash import bcrypt
from modules.sequencer.params import precision
from sys import argv

setup_db()
db_conn = make_db_connection()

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
    (r.table(kind)
      .delete()
      .run(db_conn))

es.indices.delete(index='entity', ignore=[400, 404])

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
    .run(db_conn))

(r.table('units')
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
    .run(db_conn))


(r.table('units_parameters')
    .insert([{
        'id': 'plus-params',
        'created': r.time(2014, 2, 1, 'Z'),
        'modified': r.time(2014, 2, 1, 'Z'),
        'entity_id': 'plus',
    }])
    .run(db_conn))


(r.table('cards')
    .insert([{
        'id': 'plus-video-a-1',
        'created': r.time(2014, 1, 1, 'Z'),
        'modified': r.time(2014, 1, 1, 'Z'),
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
        'modified': r.time(2014, 1, 1, 'Z'),
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
        'modified': r.time(2014, 1, 1, 'Z'),
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
    }, {
        'id': 'minus-video-a-1',
        'created': r.time(2014, 1, 1, 'Z'),
        'modified': r.time(2014, 1, 1, 'Z'),
        'entity_id': 'minus-video-a',
        'previous_id': None,
        'language': 'en',
        'name': 'How to subtract by...',
        'status': 'accepted',
        'available': True,
        'tags': ['video'],
        'unit_id': 'minus',
        'require_ids': [],
        'kind': 'video',
        'site': 'youtube',
        'video_id': 'PS5p9caXS4U'
    }, {
        'id': 'minus-choice-a-1',
        'created': r.time(2014, 1, 1, 'Z'),
        'modified': r.time(2014, 1, 1, 'Z'),
        'entity_id': 'minus-choice-a',
        'previous_id': None,
        'language': 'en',
        'name': 'Let\'s do 2 - 2',
        'status': 'accepted',
        'available': True,
        'tags': [],
        'unit_id': 'minus',
        'require_ids': [],
        'kind': 'choice',
        'body': 'What is 2 - 2?',
        'options': [{
            'value': '2',
            'correct': False,
            'feedback': 'There are two numbers.',
        }, {
            'value': '0',
            'correct': True,
            'feedback': 'We are not subtracting.',
        }, {
            'value': '1',
            'correct': False,
            'feedback': 'We are not dividing.',
        }],
        'order': 'random',
        'max_options_to_show': 4,
    }, {
        'id': 'minus-choice-b-1',
        'created': r.time(2014, 1, 1, 'Z'),
        'modified': r.time(2014, 1, 1, 'Z'),
        'entity_id': 'minus-choice-b',
        'previous_id': None,
        'language': 'en',
        'name': 'Let\'s do 3 - 1',
        'status': 'accepted',
        'available': True,
        'tags': [],
        'unit_id': 'minus',
        'require_ids': [],
        'kind': 'choice',
        'body': 'What is 3 - 1?',
        'options': [{
            'value': '2',
            'correct': True,
            'feedback': 'Yes.',
        }, {
            'value': '1',
            'correct': False,
            'feedback': 'There are two numbers.',
        }, {
            'value': '4',
            'correct': False,
            'feedback': 'There are two numbers.',
        }],
        'order': 'random',
        'max_options_to_show': 4,
    }, {
        'id': 'times-video-a-1',
        'created': r.time(2014, 1, 1, 'Z'),
        'modified': r.time(2014, 1, 1, 'Z'),
        'entity_id': 'times-video-a',
        'previous_id': None,
        'language': 'en',
        'name': 'How to multiple by...',
        'status': 'accepted',
        'available': True,
        'tags': ['video'],
        'unit_id': 'times',
        'require_ids': [],
        'kind': 'video',
        'site': 'youtube',
        'video_id': 'PS5p9caXS4U'
    }, {
        'id': 'times-choice-a-1',
        'created': r.time(2014, 1, 1, 'Z'),
        'modified': r.time(2014, 1, 1, 'Z'),
        'entity_id': 'times-choice-a',
        'previous_id': None,
        'language': 'en',
        'name': 'Let\'s do 2 * 2',
        'status': 'accepted',
        'available': True,
        'tags': [],
        'unit_id': 'times',
        'require_ids': [],
        'kind': 'choice',
        'body': 'What is 2 * 2?',
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
            'feedback': 'Yes, 2 * 2 = 4.',
        }],
        'order': 'random',
        'max_options_to_show': 4,
    }, {
        'id': 'times-choice-b-1',
        'created': r.time(2014, 1, 1, 'Z'),
        'modified': r.time(2014, 1, 1, 'Z'),
        'entity_id': 'times-choice-b',
        'previous_id': None,
        'language': 'en',
        'name': 'Let\'s do 3 * 1',
        'status': 'accepted',
        'available': True,
        'tags': [],
        'unit_id': 'times',
        'require_ids': [],
        'kind': 'choice',
        'body': 'What is 3 * 1?',
        'options': [{
            'value': '3',
            'correct': True,
            'feedback': 'Yes.',
        }, {
            'value': '1',
            'correct': False,
            'feedback': 'There are two numbers.',
        }, {
            'value': '4',
            'correct': False,
            'feedback': 'There are two numbers.',
        }],
        'order': 'random',
        'max_options_to_show': 4,
    }, {
        'id': 'slash-video-a-1',
        'created': r.time(2014, 1, 1, 'Z'),
        'modified': r.time(2014, 1, 1, 'Z'),
        'entity_id': 'slash-video-a',
        'previous_id': None,
        'language': 'en',
        'name': 'How to divide by...',
        'status': 'accepted',
        'available': True,
        'tags': ['video'],
        'unit_id': 'slash',
        'require_ids': [],
        'kind': 'video',
        'site': 'youtube',
        'video_id': 'PS5p9caXS4U'
    }, {
        'id': 'slash-choice-a-1',
        'created': r.time(2014, 1, 1, 'Z'),
        'modified': r.time(2014, 1, 1, 'Z'),
        'entity_id': 'slash-choice-a',
        'previous_id': None,
        'language': 'en',
        'name': 'Let\'s do 2 / 2',
        'status': 'accepted',
        'available': True,
        'tags': [],
        'unit_id': 'slash',
        'require_ids': [],
        'kind': 'choice',
        'body': 'What is 2 / 2?',
        'options': [{
            'value': '2',
            'correct': False,
            'feedback': 'There are two numbers.',
        }, {
            'value': '0',
            'correct': False,
            'feedback': 'We are not subtracting.',
        }, {
            'value': '1',
            'correct': True,
            'feedback': 'Yes, 2 / 2 = 1.',
        }],
        'order': 'random',
        'max_options_to_show': 4,
    }, {
        'id': 'slash-choice-b-1',
        'created': r.time(2014, 1, 1, 'Z'),
        'modified': r.time(2014, 1, 1, 'Z'),
        'entity_id': 'slash-choice-b',
        'previous_id': None,
        'language': 'en',
        'name': 'Let\'s do 3 / 1',
        'status': 'accepted',
        'available': True,
        'tags': [],
        'unit_id': 'slash',
        'require_ids': [],
        'kind': 'choice',
        'body': 'What is 3 / 1?',
        'options': [{
            'value': '3',
            'correct': True,
            'feedback': 'Yes.',
        }, {
            'value': '1',
            'correct': False,
            'feedback': 'There are two numbers.',
        }, {
            'value': '4',
            'correct': False,
            'feedback': 'There are two numbers.',
        }],
        'order': 'random',
        'max_options_to_show': 4,
    }])
    .run(db_conn))


(r.table('cards_parameters')
    .insert([{
        'id': 'plus-video-a-params',
        'created': r.time(2014, 1, 1, 'Z'),
        'modified': r.time(2014, 1, 1, 'Z'),
        'entity_id': 'plus-video-a',
    }, {
        'id': 'plus-choice-a-params',
        'created': r.time(2014, 1, 1, 'Z'),
        'modified': r.time(2014, 1, 1, 'Z'),
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
        'modified': r.time(2014, 1, 1, 'Z'),
        'entity_id': 'plus-choice-b',
        'guess_distribution': {
            str(h): 1 - (0.5 - h) ** 2
            for h in [h / precision for h in range(1, precision)]
        },
        'slip_distribution': {
            str(h): 1 - (0.25 - h) ** 2
            for h in [h / precision for h in range(1, precision)]
        }
    }, {
        'id': 'minus-video-a-params',
        'created': r.time(2014, 1, 1, 'Z'),
        'modified': r.time(2014, 1, 1, 'Z'),
        'entity_id': 'minus-video-a',
    }, {
        'id': 'minus-choice-a-params',
        'created': r.time(2014, 1, 1, 'Z'),
        'modified': r.time(2014, 1, 1, 'Z'),
        'entity_id': 'minus-choice-a',
        'guess_distribution': {
            str(h): 1 - (0.5 - h) ** 2
            for h in [h / precision for h in range(1, precision)]
        },
        'slip_distribution': {
            str(h): 1 - (0.25 - h) ** 2
            for h in [h / precision for h in range(1, precision)]
        }
    }, {
        'id': 'minus-choice-b-params',
        'created': r.time(2014, 1, 1, 'Z'),
        'modified': r.time(2014, 1, 1, 'Z'),
        'entity_id': 'minus-choice-b',
        'guess_distribution': {
            str(h): 1 - (0.5 - h) ** 2
            for h in [h / precision for h in range(1, precision)]
        },
        'slip_distribution': {
            str(h): 1 - (0.25 - h) ** 2
            for h in [h / precision for h in range(1, precision)]
        }
    }, {
        'id': 'times-video-a-params',
        'created': r.time(2014, 1, 1, 'Z'),
        'modified': r.time(2014, 1, 1, 'Z'),
        'entity_id': 'times-video-a',
    }, {
        'id': 'times-choice-a-params',
        'created': r.time(2014, 1, 1, 'Z'),
        'modified': r.time(2014, 1, 1, 'Z'),
        'entity_id': 'times-choice-a',
        'guess_distribution': {
            str(h): 1 - (0.5 - h) ** 2
            for h in [h / precision for h in range(1, precision)]
        },
        'slip_distribution': {
            str(h): 1 - (0.25 - h) ** 2
            for h in [h / precision for h in range(1, precision)]
        }
    }, {
        'id': 'times-choice-b-params',
        'created': r.time(2014, 1, 1, 'Z'),
        'modified': r.time(2014, 1, 1, 'Z'),
        'entity_id': 'times-choice-b',
        'guess_distribution': {
            str(h): 1 - (0.5 - h) ** 2
            for h in [h / precision for h in range(1, precision)]
        },
        'slip_distribution': {
            str(h): 1 - (0.25 - h) ** 2
            for h in [h / precision for h in range(1, precision)]
        }
    }, {
        'id': 'slash-video-a-params',
        'created': r.time(2014, 1, 1, 'Z'),
        'modified': r.time(2014, 1, 1, 'Z'),
        'entity_id': 'slash-video-a',
    }, {
        'id': 'slash-choice-a-params',
        'created': r.time(2014, 1, 1, 'Z'),
        'modified': r.time(2014, 1, 1, 'Z'),
        'entity_id': 'slash-choice-a',
        'guess_distribution': {
            str(h): 1 - (0.5 - h) ** 2
            for h in [h / precision for h in range(1, precision)]
        },
        'slip_distribution': {
            str(h): 1 - (0.25 - h) ** 2
            for h in [h / precision for h in range(1, precision)]
        }
    }, {
        'id': 'slash-choice-b-params',
        'created': r.time(2014, 1, 1, 'Z'),
        'modified': r.time(2014, 1, 1, 'Z'),
        'entity_id': 'slash-choice-b',
        'guess_distribution': {
            str(h): 1 - (0.5 - h) ** 2
            for h in [h / precision for h in range(1, precision)]
        },
        'slip_distribution': {
            str(h): 1 - (0.25 - h) ** 2
            for h in [h / precision for h in range(1, precision)]
        }
    }])
    .run(db_conn))

(r.table('sets')
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
    .run(db_conn))


(r.table('sets_parameters')
    .insert([{
        'id': 'basic-math-params',
        'created': r.time(2014, 1, 1, 'Z'),
        'modified': r.time(2014, 1, 1, 'Z'),
        'entity_id': 'basic-math',
    }])
    .run(db_conn))

(r.table('topics')
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
    .run(db_conn))


(r.table('posts')
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
        'response': True,
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
    .run(db_conn))


(r.table('follows')
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
    .run(db_conn))

(r.table('notices')
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
    .run(db_conn))

(r.table('users_sets')
    .insert([{
        'id': 'doris-sets',
        'created': r.time(2014, 1, 1, 'Z'),
        'modified': r.time(2014, 1, 1, 'Z'),
        'user_id': 'doris',
        'set_ids': ['basic-math'],
    }])
    .run(db_conn))

# id, created, modified
# user_id, card_id, unit_id, response, score, learned
if len(argv) > 1 and argv[1] == 'learn_mode':
    (r.table('responses')
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
        .run(db_conn))

close_db_connection(db_conn)
