from models.follow import Follow
from database.notice import insert_notice

# TODO-2 send out notices via email per user preference


def send_notices(db_conn, entity_id, entity_kind, notice_kind, notice_data):
    """
    When an event occurs, send notices outs.
    """

    user_ids = Follow.get_user_ids_by_entity(db_conn,
                                             entity_id=entity_id,
                                             entity_kind=entity_kind)
    for user_id in user_ids:
        notice, errors = insert_notice({
            'user_id': user_id,
            'kind': notice_kind,
            'data': notice_data,
        }, db_conn)
        if errors:
            raise Exception(errors)
