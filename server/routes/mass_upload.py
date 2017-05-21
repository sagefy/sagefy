from framework.routes import post, abort
from framework.session import get_current_user
from modules.util import uniqid
import rethinkdb as r


# TODO-1 delete this file
# TODO-2 remove temporary auto approvers
reviewer_a_id = 'uVpp1Zovc4S3jihP8X29tXGf'
reviewer_b_id = 'ikFGjpOHa3YQlpuCNkHE0Bzp'


def inject_unit(unit, db_conn):
    """

    """
    entity_id = uniqid()
    version_id = uniqid()
    r.db('sagefy').table('units').insert({
        'id': version_id,
        'created': r.now(),
        'modified': r.now(),
        'entity_id': entity_id,
        'language': 'en',
        'name': unit['name'],
        'status': 'pending',
        'available': True,
        'tags': [],
        'body': unit['body'],
        'require_ids': unit.get('require_ids') or [],
    }).run(db_conn)
    return entity_id, version_id


def inject_video_card(unit_id, card, db_conn):
    """

    """
    entity_id = uniqid()
    version_id = uniqid()
    r.db('sagefy').table('cards').insert({
        'id': version_id,
        'created': r.now(),
        'modified': r.now(),
        'unit_id': unit_id,
        'require_ids': [],
        'kind': 'video',
        'site': 'youtube',
        'video_id': card['video_id'],
        'entity_id': entity_id,
        'language': 'en',
        'name': 'Primary Video',
        'status': 'pending',
        'available': True,
        'tags': []
    }).run(db_conn)
    return entity_id, version_id


def inject_choice_card(unit_id, card, db_conn):
    """

    """
    entity_id = uniqid()
    version_id = uniqid()
    r.db('sagefy').table('cards').insert({
        'id': version_id,
        'created': r.now(),
        'modified': r.now(),
        'unit_id': unit_id,
        'require_ids': [],
        'kind': 'choice',
        'body': card['body'],
        'options': [{
            'value': option['value'],
            'feedback': option['feedback'],
            'correct': option['correct'] in ('Y', True),
        } for option in card['options']],
        'order': 'random',
        'max_options_to_show': 4,
        'entity_id': entity_id,
        'language': 'en',
        'name': card['body'],
        'status': 'pending',
        'available': True,
        'tags': []
    }).run(db_conn)
    return entity_id, version_id


def inject_topic(kind, entity, entity_id, user_id, db_conn):
    topic_id = uniqid()
    entity_body = entity.get('body', 'Video')

    r.db('sagefy').table('topics').insert({
        'id': topic_id,
        'created': r.now(),
        'modified': r.now(),
        'user_id': user_id,
        'name': 'Create "%s"' % entity_body,
        'entity': {
            'id': entity_id,
            'kind': 'unit' if kind == 'unit' else 'card'
        }
    }).run(db_conn)

    return topic_id


def inject_proposal(kind, entity, user_id, topic_id, version_id, db_conn):
    proposal_id = uniqid()
    entity_body = entity.get('body', 'Video')

    r.db('sagefy').table('posts').insert({
        'id': proposal_id,
        'created': r.now(),
        'modified': r.now(),
        'user_id': user_id,
        'topic_id': topic_id,
        'kind': 'proposal',
        'entity_versions': [{
            'id': version_id,
            'kind': 'unit' if kind == 'unit' else 'card',
        }],
        'body': 'Create "%s"' % entity_body,
        'name': 'Create "%s"' % entity_body,
    }).run(db_conn)

    return proposal_id


def inject_votes(topic_id, proposal_id, db_conn):
    my_data = {
        'created': r.now(),
        'modified': r.now(),
        'topic_id': topic_id,
        'body': 'I agree.',
        'kind': 'vote',
        'replies_to_id': proposal_id,
        'response': True
    }

    my_data['id'] = uniqid()
    my_data['user_id'] = reviewer_a_id
    r.db('sagefy').table('posts').insert(my_data).run(db_conn)

    my_data['id'] = uniqid()
    my_data['user_id'] = reviewer_b_id
    r.db('sagefy').table('posts').insert(my_data).run(db_conn)


def update_status(kind, version_id, db_conn):
    if kind != 'unit' and kind != 'card':
        raise Exception('must be a unit or card')
    r.db('sagefy').table(kind + 's').get(version_id).update({
        'modified': r.now(),
        'status': 'accepted',
    }).run(db_conn)


@post('/s/mass_upload')
def create_topic_route(request):
    """

    """

    db_conn = request['db_conn']

    current_user = get_current_user(request)
    if not current_user:
        return abort(401)

    user_id = current_user['id']

    if user_id != "NNKkHsjE3pEOW0wsPaQJm9MD":
        return abort(403)

    data = request['params']
    if not data:
        return abort(404)

    for key, unit in data.get('units').items():
        unit_entity_id, unit_version_id = inject_unit(unit, db_conn)
        topic_id = inject_topic('unit', unit, unit_entity_id, user_id, db_conn)
        proposal_id = inject_proposal('unit', unit, user_id, topic_id,
                                      unit_version_id, db_conn)
        inject_votes(topic_id, proposal_id, db_conn)
        update_status('unit', unit_version_id, db_conn)

        for card in unit.get('video', []):
            kind = 'video'
            entity_id, version_id = inject_video_card(unit_entity_id, card,
                                                      db_conn)
            topic_id = inject_topic(kind, card, entity_id, user_id, db_conn)
            proposal_id = inject_proposal(kind, card, user_id, topic_id,
                                          version_id, db_conn)
            inject_votes(topic_id, proposal_id, db_conn)
            update_status('card', version_id, db_conn)

        for card in unit.get('choice', []):
            kind = 'choice'
            entity_id, version_id = inject_choice_card(unit_entity_id, card,
                                                       db_conn)
            topic_id = inject_topic(kind, card, entity_id, user_id, db_conn)
            proposal_id = inject_proposal(kind, card, user_id, topic_id,
                                          version_id, db_conn)
            inject_votes(topic_id, proposal_id, db_conn)
            update_status('card', version_id, db_conn)

    return 200, 'OK'
