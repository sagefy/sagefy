from framework.routes import get, post, put, delete, abort
from framework.session import get_current_user
from database.user import set_learning_context, get_user
from database.user_subjects import insert_user_subject, list_user_subjects, \
    remove_user_subject, list_user_subjects_entity
from database.subject import deliver_subject, get_latest_accepted_subject
from modules.sequencer.traversal import traverse
from modules.sequencer.card_chooser import choose_card
from modules.util import convert_slug_to_uuid, convert_uuid_to_slug


@get('/s/users/{user_id}/subjects')
def get_user_subjects_route(request, user_id):
    """
    Get the list of subjects the user has added.

    NEXT STATE
    GET Choose Subject
        -> POST Choose Subject
    """

    db_conn = request['db_conn']
    current_user = get_current_user(request)
    if not current_user or current_user['id'] != convert_slug_to_uuid(user_id):
        user = get_user(db_conn, {'id': user_id})
        if not user:
            return abort(404)
        if (user != current_user and
                user['settings']['view_subjects'] != 'public'):
            return abort(403)
    else:
        user = current_user
        if not current_user:
            return abort(401)
    params = request['params']
    user_subjects = list_user_subjects_entity(db_conn, user_id, params)
    response = {
        'subjects': [
            deliver_subject(subject)
            for subject in user_subjects
        ]
    }
    if current_user == user:
        next_ = {
            'method': 'POST',
            'path': '/s/users/{user_id}/subjects/{subject_id}'
                    .format(user_id=current_user['id'],
                            subject_id='{subject_id}'),
        }
        set_learning_context(current_user, next=next_)
        response['next'] = next_
    return 200, response


@post('/s/users/{user_id}/subjects/{subject_id}')
def add_subject_route(request, user_id, subject_id):
    """
    Add a subject to the learner's list of subjects.
    """

    db_conn = request['db_conn']
    current_user = get_current_user(request)
    if not current_user:
        return abort(401)
    if convert_slug_to_uuid(user_id) != current_user['id']:
        return abort(403)
    subject = get_latest_accepted_subject(db_conn, subject_id)
    if not subject:
        return abort(404)
    # TODO-1 handle if subject already added
    user_subject, errors = insert_user_subject(db_conn, user_id, subject_id)
    if errors:
        return 400, {
            'errors': errors,
            'ref': 'zCFUbLBTg9n2DnTkQYbqO4X9'
        }
    return 200, {'user_subject': user_subject}


@put('/s/users/{user_id}/subjects/{subject_id}')
def select_subject_route(request, user_id, subject_id):
    """
    Select the subject to work on.

    NEXT STATE
    POST Choose Subject   (Update Learner Context)
        -> GET Choose Subject ...when subject is complete
        -> GET Choose Unit    ...when in learn or review mode
        -> GET Learn Card     ...when in diagnosis
            (Unit auto chosen)
    """

    db_conn = request['db_conn']
    current_user = get_current_user(request)
    if not current_user:
        return abort(401)
    subject = get_latest_accepted_subject(db_conn, subject_id)
    set_learning_context(current_user, subject=subject)
    buckets = traverse(db_conn, current_user, subject)
    # When in diagnosis, choose the unit and card automagically.
    if buckets.get('diagnose'):
        unit = buckets['diagnose'][0]
        card = choose_card(db_conn, current_user, unit)
        next_ = {
            'method': 'GET',
            'path': '/s/cards/{card_id}/learn'
                    .format(card_id=convert_uuid_to_slug(card['entity_id'])),
        }
        set_learning_context(
            current_user,
            next=next_, unit=unit, card=card)
    # When in learn or review mode, lead me to choose a unit.
    elif buckets.get('review') or buckets.get('learn'):
        next_ = {
            'method': 'GET',
            'path': '/s/subjects/{subject_id}/units'
                    .format(subject_id=convert_uuid_to_slug(subject_id)),
        }
        set_learning_context(current_user, next=next_)
    # If the subject is complete, lead the learner to choose another subject.
    else:
        next_ = {
            'method': 'GET',
            'path': '/s/users/{user_id}/subjects'
                    .format(user_id=convert_uuid_to_slug(current_user['id'])),
        }
        set_learning_context(current_user, next=next_, unit=None, subject=None)
    return 200, {'next': next_}


@delete('/s/users/{user_id}/subjects/{subject_id}')
def remove_subject_route(request, user_id, subject_id):
    """
    Remove a subject from the learner's list of subjects.
    """

    db_conn = request['db_conn']
    current_user = get_current_user(request)
    if not current_user:
        return abort(401)
    if user_id != current_user['id']:
        return abort(403)
    user_subjects = list_user_subjects(db_conn, user_id)
    if not user_subjects:
        return 404, {
            'errors': [{'message': 'User does not have subjects.'}],
            'ref': '8huZbvEAYOP8LcZb2sXbqNOC'
        }
    matches = [
        us
        for us in user_subjects
        if convert_uuid_to_slug(us['subject_id']) == subject_id
    ]
    if not matches:
        return abort(404)
    user_subject, errors = remove_user_subject(db_conn, user_id, subject_id)
    if errors:
        return 400, {
            'errors': errors,
            'ref': 'qIfll1e7dbP9V9jmC8FkCwsa'
        }
    return 200, {}
