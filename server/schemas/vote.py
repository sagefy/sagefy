from schemas.post import schema as post_schema
from schemas.post import is_valid_reply
from modules.util import extend


def is_unique_vote(db_conn, schema, data):
    """
    Ensure a user can only vote once per proposal.
    """

    query = (r.table(post_schema['tablename'])
              .filter(r.row['user_id'] == data['user_id'])
              .filter(r.row['replies_to_id'] == data['replies_to_id'])
              .filter(r.row['kind'] == 'vote'))
    documents = [doc for doc in query.run(db_conn)]
    if documents:
        return [{'message': 'You already have a vote on this proposal.'}]
    return []


def is_valid_reply_kind(db_conn, schema, data):
    """
    A vote can reply to a proposal.
    A vote cannot reply to a proposal that is accepted or declined.
    A user cannot vote on their own proposal.
    """

    query = (r.table(post_schema['tablename'])
              .get(data['replies_to_id']))
    proposal_data = query.run(db_conn)
    if not proposal_data:
        return [{'message': 'No proposal found.'}]
    if proposal_data['kind'] != 'proposal':
        return [{'message': 'A vote must reply to a proposal.'}]
    if proposal_data['user_id'] == data['user_id']:
        return [{'message': 'You cannot vote on your own proposal.'}]
    tablename = '%ss' % proposal_data['entity_versions'][0]['kind']
    version_id = proposal_data['entity_versions'][0]['id']
    entity_version = get_version(db_conn, tablename, version_id)
    if not entity_version:
        return [{'message': 'No entity version for proposal.'}]
    if entity_version['status'] in ('accepted', 'declined'):
        return [{'message': 'Proposal is already complete.'}]
    return []


schema = extend({}, post_schema, {
    'fields': {
        'response': {}
    },
    'validate': (
        is_valid_reply,
        is_unique_vote,
        is_valid_reply_kind,
    ),
})
