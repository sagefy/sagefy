# MMM
from framework.routes import get, post, put, delete, abort
from framework.session import get_current_user
from database.user import set_learning_context
from database.user_subjects import insert_user_subjects, get_user_subjects, \
    append_user_subjects, remove_user_subjects, \
    list_user_subjects_entity


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
    if not current_user:
        return abort(401)

    if user_id != current_user['id']:
        return abort(403)

    next_ = {
        'method': 'POST',
        'path': '/s/users/{user_id}/subjects/{subject_id}'
                .format(user_id=current_user['id'],
                        subject_id='{subject_id}'),
    }
    set_learning_context(current_user, next=next_)

    user_subject = get_user_subjects(user_id, db_conn)
    if not user_subject:
        return 200, {'subjects': [], 'next': next_}
    return 200, {
        'subjects': [
            subject.deliver()
            for subject in list_user_subjects_entity(
                user_id,
                request['params'],
                db_conn)],
        'next': next_,
    }


@post('/s/users/{user_id}/subjects/{subject_id}')
def add_subject_route(request, user_id, subject_id):
    """
    Add a subject to the learner's list of subjects.
    """

    db_conn = request['db_conn']

    current_user = get_current_user(request)
    if not current_user:
        return abort(401)

    if user_id != current_user['id']:
        return abort(403)

    subject = Subject.get(db_conn, entity_id=subject_id)
    if not subject:
        return abort(404)

    user_subject = get_user_subjects(user_id, db_conn)
    if user_subject and subject_id in user_subject['subject_ids']:
        return 400, {
            'errors': [{
                'name': 'subject_id',
                'message': 'Subject is already added.',
            }],
            'ref': 'kPZ95zM3oxFDGGl8vBdR3J3o',
        }

    # TODO-2 move some of this logic to the database file
    if user_subject:
        user_subject, errors = append_user_subjects(
            user_id, subject_id, db_conn)
    else:
        user_subject, errors = insert_user_subjects({
            'user_id': user_id,
            'subject_ids': [subject_id],
        }, db_conn)

    if errors:
        return 400, {
            'errors': errors,
            'ref': 'zCFUbLBTg9n2DnTkQYbqO4X9'
        }

    return 200, {'subjects': user_subject['subject_ids']}


@put('/s/users/{user_id}/subjects/{subject_id}')
def select_subject_route(request, user_id, subject_id):
    """
    Select the subject to work on.

    NEXT STATE
    POST Choose Subject   (Update Learner Context)
        -> GET View Subject Tree
    """

    db_conn = request['db_conn']

    current_user = get_current_user(request)
    if not current_user:
        return abort(401)

    subject = get_latest_accepted('subjects', db_conn, subject_id)
    next_ = {
        'method': 'GET',
        'path': '/s/subjects/{subject_id}/tree'
                .format(subject_id=subject_id),
    }
    set_learning_context(current_user, subject=subject.data, next=next_)

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

    user_subject = get_user_subjects(user_id, db_conn)
    if not user_subject:
        return 404, {
            'errors': [{'message': 'User does not have subjects.'}],
            'ref': '8huZbvEAYOP8LcZb2sXbqNOC'
        }

    if subject_id not in user_subject['subject_ids']:
        return abort(404)

    user_subject, errors = remove_user_subjects(user_id, subject_id, db_conn)

    if errors:
        return 400, {
            'errors': errors,
            'ref': 'qIfll1e7dbP9V9jmC8FkCwsa'
        }

    return 200, {'subjects': user_subject['subject_ids']}
