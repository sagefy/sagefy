from schemas.index import schema as default
from modules.util import extend


def is_valid_reply(db_conn, schema, data):
    """
    A reply must belong to the same topic.
    - A post can reply to a post, proposal, or vote.
    - A proposal can reply to a post, proposal, or vote.
    - A vote may only reply to a proposal.
    """

    if data.get('replies_to_id'):
        query = (r.table('posts')
                  .get(data['replies_to_id']))
        post_data = query.run(db_conn)
        if post_data['topic_id'] != data['topic_id']:
            return [{'message': 'A reply must be in the same topic.'}]
    return []


schema = extend({}, default, {
    'tablename': 'posts',
    'fields': {
        'user_id': {},
        'topic_id': {},
        'body': {},
        'kind': {},
        'replies_to_id': {},
    },
    'validate': (is_valid_reply),
})
