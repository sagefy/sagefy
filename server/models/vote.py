from models.post import Post
from modules.validations import is_required, is_string, is_boolean
import rethinkdb as r
import framework.database as database
from modules.entity import get_version  # TODO-2 this may cause a problem


class Vote(Post):
    """
    A vote or response on a proposal.
    """

    # For votes, a body is not required but optional,
    # But a replies to id is required
    schema = dict(Post.schema.copy(), **{
        # A vote does not require a body
        'body': {
            'validate': (is_string,)
        },

        # But a vote does require a proposal
        'replies_to_id': {
            'validate': (is_required, is_string,)
        },

        # The only true unique field of a vote...
        # Where True is yes, False is no
        'response': {
            'validate': (is_boolean,),
            'default': None
        }
    })

    def __init__(self, fields=None):
        """
        When creating a new vote,
        set the correct kiwnd.
        """

        super().__init__(fields)
        self.kind = 'vote'

    def validate(self):
        errors = super().validate()
        if not errors:
            errors += self.is_unique_vote()
        if not errors:
            errors += self.is_valid_reply_kind()
        return errors

    def is_unique_vote(self):
        """
        Ensure a user can only vote once per proposal.
        """

        query = (self.table
                     .filter(r.row['user_id'] == self['user_id'])
                     .filter(r.row['replies_to_id'] == self['replies_to_id'])
                     .filter(r.row['kind'] == 'vote'))
        documents = [doc for doc in query.run(database.db_conn)]
        if documents:
            return [{'message': 'You already have a vote on this proposal.'}]
        return []

    def is_valid_reply_kind(self):
        """
        A vote can reply to a proposal.
        A vote cannot reply to a proposal that is accepted or declined.
        A user cannot vote on their own proposal.
        """

        query = (self.table
                     .get(self['replies_to_id']))
        proposal_data = query.run(database.db_conn)
        if not proposal_data:
            return [{'message': 'No proposal found.'}]
        if proposal_data['kind'] != 'proposal':
            return [{'message': 'A vote must reply to a proposal.'}]
        if proposal_data['user_id'] == self['user_id']:
            return [{'message': 'You cannot vote on your own proposal.'}]
        entity_version = get_version(proposal_data['entity_version']['kind'],
                                     proposal_data['entity_version']['id'])
        if not entity_version:
            return [{'message': 'No entity version for proposal.'}]
        if entity_version['status'] in ('accepted', 'declined'):
            return [{'message': 'Proposal is already complete.'}]
        return []
