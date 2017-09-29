from datetime import datetime
import uuid
from modules.sequencer.params import precision
import psycopg2.extras
from database.util import save_row
from passlib.hash import bcrypt
from modules.util import convert_slug_to_uuid


user_id = '1SbHc12NTLKMtDJmE83AJg'


def raw_insert_user(db_conn, user):
    query = """
        INSERT INTO users
        (  id  ,   created  ,   modified  ,
           name  ,   email,   password  ,   settings)
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
        'password': bcrypt.encrypt(user.get('password')),
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
             %(unit_id)s, %(require_ids)s, %(kind)s, %(data)s)
            RETURNING *;
        """
        params = {
            'version_id': card.get('version_id', uuid.uuid4()),
            'created': card.get('created', datetime.utcnow()),
            'modified': card.get('modified', datetime.utcnow()),
            'entity_id': card.get('entity_id'),
            'previous_id': card.get('previous_id'),
            'language': 'en',
            'status': 'accepted',
            'available': True,
            'tags': [],
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
             %(body)s, %(require_ids)s)
            RETURNING *;
        """
        params = {
            'version_id': unit.get('version_id', uuid.uuid4()),
            'created': unit.get('created', datetime.utcnow()),
            'modified': unit.get('modified', datetime.utcnow()),
            'entity_id': unit.get('entity_id'),
            'previous_id': unit.get('previous_id'),
            'language': 'en',
            'status': 'accepted',
            'available': True,
            'tags': [],
            'name': unit.get('name'),
            'user_id': unit.get('user_id', convert_slug_to_uuid(user_id)),
            'body': unit.get('body'),
            'require_ids': unit.get('require_ids', []),
        }
        save_row(db_conn, query, params)
