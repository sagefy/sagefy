from schemas.notice import schema as notice_schema
from database.util import insert_document, update_document, deliver_fields, \
    get_document
from modules.content import get as c
from copy import deepcopy

# done-- implement create_topic notice
# done-- implement create_proposal notice
# done-- implement block_proposal notice
# TODO-2 implement decline_proposal notice
# done-- implement accept_proposal notice
# TODO-2 implement create_post notice
# TODO-2 implement come_back notice


"""
Required data fields per kind:

create_topic: user_name, topic_name, entity_kind, entity_name
create_proposal: user_name, proposal_name, entity_kind, entity_name
block_proposal: user_name, proposal_name, entity_kind, entity_name
decline_proposal: user_name, proposal_name, entity_kind, entity_name
accept_proposal: proposal_name, entity_kind, entity_name
create_post: user_name, topic_name, entity_kind, entity_name
come_back: -
"""


def get_notice(params, db_conn):
    """
    Get the user matching the parameters.
    """

    tablename = notice_schema['tablename']
    return get_document(tablename, params, db_conn)


def insert_notice(data, db_conn):
    """
    Create a new notice.

    *M2P Insert a Notice [hidden]

        INSERT INTO notices
        (  user_id  ,   kind  ,   data  )
        VALUES
        (%(user_id)s, %(kind)s, %(data)s);
    """

    schema = notice_schema
    return insert_document(schema, data, db_conn)


def list_notices(params, db_conn):
    """
    Get a list of models matching the provided arguments.
    Also adds pagination capabilities.
    Returns empty array when no models match.


    *M2P List Notices by User ID

        SELECT *
        FROM notices
        WHERE user_id = %(user_id)s
        ORDER BY created DESC;
        /* TODO OFFSET LIMIT */
    """

    limit = params.get('limit') or 10
    skip = params.get('skip') or 0
    schema = notice_schema
    query = (r.table(schema['tablename'])
              .filter(r.row['user_id'] == params.get('user_id'))
              .filter(r.row['kind'] == params.get('kind')
                      if params.get('kind') is not None else True)
              .filter(r.row['tags'].contains(params.get('tag'))
                      if params.get('tag') is not None else True)
              .filter(r.row['read'] == params.get('read')
                      if params.get('read') is not None else True)
              .order_by(r.desc('created'))
              .skip(skip)
              .limit(limit))
    return list(query.run(db_conn))


def mark_notice_as_read(notice, db_conn):
    """
    Marks the notice as read.

    *M2P Mark Notice as Read

        UPDATE notices
        SET read = TRUE
        WHERE id = %(id)s;
    """

    schema = notice_schema
    return update_document(schema, notice, {'read': True}, db_conn)


def mark_notice_as_unread(notice, db_conn):
    """
    Marks the notice as unread.

    *M2P Mark Notice as Unread

        UPDATE notices
        SET read = FALSE
        WHERE id = %(id)s;
    """

    schema = notice_schema
    return update_document(schema, notice, {'read': False}, db_conn)


def get_notice_body(notice):
    """
    Get the copy associated with this notice.
    """

    return c('notice_' + notice['kind']).format(**notice['data'])


def deliver_notice(notice, access=None):
    """
    Add the notice body to the notice before delivering.
    """

    schema = notice_schema
    notice = deepcopy(notice)
    notice['body'] = get_notice_body(notice)
    return deliver_fields(schema, notice, access)
