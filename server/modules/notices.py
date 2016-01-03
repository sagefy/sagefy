from models.follow import Follow
from models.notice import Notice

# TODO-2 send out notices via email per user preference


def send_notices(entity_id, entity_kind, notice_kind, notice_data):
    """
    When an event occurs, send notices outs.
    """

    user_ids = Follow.get_user_ids_by_entity(entity_id=entity_id,
                                             entity_kind=entity_kind)
    for user_id in user_ids:
        notice, errors = Notice.insert({
            'user_id': user_id,
            'kind': notice_kind,
            'data': notice_data,
        })
        if errors:
            raise Exception(errors)
