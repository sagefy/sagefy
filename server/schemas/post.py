from schemas.index import schema as default
from modules.validations import is_required, is_string, is_one_of, \
    has_min_length
from modules.util import extend



def is_valid_topic_id(schema, data, db_conn):
    """
    TODO-3 Ensure the topic is valid.
           Is there a way to allow for 'in memory only' topic?
    (We're currently validating this in the route for now...)
    """

    return []


def is_valid_reply(schema, data, db_conn):
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
        if not post_data:
            return [{'message': 'Replying to a non-existant post.'}]
        if post_data['topic_id'] != data['topic_id']:
            return [{'message': 'A reply must be in the same topic.'}]
    return []


schema = extend({}, default, {
    'tablename': 'posts',
    'fields': {
        'user_id': {  # TODO-2 validate foreign
            'validate': (is_required, is_string,)
        },
        'topic_id': {
            'validate': (is_required, is_string,)
        },
        'body': {
            'validate': (is_required, is_string, (has_min_length, 1),)
        },
        'kind': {
            'validate': (is_required, is_string,
                         (is_one_of, 'post', 'proposal', 'vote')),
            'default': 'post'
        },
        'replies_to_id': {
            'validate': (is_string,)
        }
    },
    'validate': (is_valid_topic_id, is_valid_reply),
})
