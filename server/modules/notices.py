from database.notice import insert_notice
from database.follow import get_user_ids_by_followed_entity
# TODO-2 send out notices via email per user preference


def send_notices(db_conn, entity_id, entity_kind, notice_kind, notice_data):
    """
    When an event occurs, send notices outs.
    """

    user_ids = get_user_ids_by_followed_entity(db_conn, entity_id, entity_kind)
    for user_id in user_ids:
        notice, errors = insert_notice(db_conn, {
            'user_id': user_id,
            'kind': notice_kind,
            'data': notice_data,
        })
        if errors:
            raise Exception(errors)
