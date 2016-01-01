from modules.model import Model
from modules.validations import is_required, is_string, is_boolean, is_list, \
    is_one_of, is_list_of_strings, is_dict
import rethinkdb as r
import framework.database as database
from modules.content import get as c

# done-- implement create_topic notice
# TODO-1 implement create_proposal notice
# done-- implement block_proposal notice
# TODO-1 implement decline_proposal notice
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


class Notice(Model):
    tablename = 'notices'

    schema = dict(Model.schema.copy(), **{
        'user_id': {
            'validate': (is_required, is_string,)
        },
        'kind': {
            'validate': (is_required, is_string, (
                is_one_of,
                'create_topic',
                'create_proposal',
                'block_proposal',
                'decline_proposal',
                'accept_proposal',
                'create_post',
                'come_back',
            ))
        },
        'data': {
            'validate': (is_dict,),
            'default': {},
        },
        'read': {
            'validate': (is_boolean,),
            'default': False
        },
        'tags': {
            'validate': (is_list, is_list_of_strings),
            'default': []
        }
    })

    @classmethod
    def list(cls, user_id=None, limit=10, skip=0, read=None, tag=None,
             kind=None, **params):
        """
        Get a list of models matching the provided arguments.
        Also adds pagination capabilities.
        Returns empty array when no models match.
        """

        query = (cls.table
                    .filter(r.row['user_id'] == user_id)
                    .filter(r.row['kind'] == kind
                            if kind is not None else True)
                    .filter(r.row['tags'].contains(tag)
                            if tag is not None else True)
                    .filter(r.row['read'] == read
                            if read is not None else True)
                    .order_by(r.desc('created'))
                    .skip(skip)
                    .limit(limit))
        fields_list = query.run(database.db_conn)
        return [cls(fields) for fields in fields_list]

    def mark_as_read(self):
        """
        Marks the notice as read.
        """

        self['read'] = True
        return self.save()

    def mark_as_unread(self):
        """
        Marks the notice as unread.
        """

        self['read'] = False
        return self.save()

    def get_body(self):
        """
        Get the copy associated with this notice.
        """

        return c('notice_' + self['kind']).format(**self['data'])

    def deliver(self, access=None):
        """
        Add the notice body to the notice before delivering.
        """

        data = super().deliver(access)
        data['body'] = self.get_body()
        return data
