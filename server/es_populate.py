import rethinkdb as r
from framework.database import setup_db, make_db_connection, \
    close_db_connection
from framework.elasticsearch import es
from modules.util import json_prep, pick
from models.user import get_avatar

setup_db()
db_conn = make_db_connection()

# Empty the database
es.indices.delete(index='entity', ignore=[400, 404])

# Add users
users = r.table('users').run(db_conn)
for user in users:
    data = pick(json_prep(user), ('id', 'name'))
    data['avatar'] = get_avatar(user['email'])
    es.index(
        index='entity',
        doc_type='user',
        body=data,
        id=user['id'],
    )

# Add units
units = (r.table('units')
          .filter(r.row['status'].eq('accepted'))
          .group('entity_id')
          .max('created')
          .default(None)
          .ungroup()
          .map(r.row['reduction'])
          .run(db_conn))

for unit in units:
    es.index(
        index='entity',
        doc_type='unit',
        body=json_prep(unit),
        id=unit['entity_id'],
    )

# Add cards
cards = (r.table('cards')
          .filter(r.row['status'].eq('accepted'))
          .group('entity_id')
          .max('created')
          .default(None)
          .ungroup()
          .map(r.row['reduction'])
          .run(db_conn))
for card in cards:
    es.index(
        index='entity',
        doc_type='card',
        body=json_prep(card),
        id=card['entity_id'],
    )

# Add sets
sets = (r.table('sets')
         .filter(r.row['status'].eq('accepted'))
         .group('entity_id')
         .max('created')
         .default(None)
         .ungroup()
         .map(r.row['reduction'])
         .run(db_conn))
for set_ in sets:
    es.index(
        index='entity',
        doc_type='set',
        body=json_prep(set_),
        id=set_['entity_id'],
    )

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


close_db_connection(db_conn)
