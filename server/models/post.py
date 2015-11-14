from modules.model import Model
from modules.validations import is_required, is_string, is_one_of
from framework.elasticsearch import es
from modules.util import json_prep


class Post(Model):
    """A discussion post."""
    tablename = 'posts'

    schema = dict(Model.schema.copy(), **{
        'user_id': {
            'validate': (is_required, is_string,)
        },
        'topic_id': {
            'validate': (is_required, is_string,)
        },
        'body': {
            'validate': (is_required, is_string,)
        },
        'kind': {
            'validate': (is_required, is_string,
                         (is_one_of, 'post', 'proposal', 'vote', 'flag')),
            'default': 'post'
        },
        'replies_to_id': {
            'validate': (is_string,)  # TODO@ validate id is real & in topic
        }
    })

    def validate(self):
        errors = super().validate()
        if not errors:
            errors += self.is_valid_reply_kind()
        return errors

    def is_valid_reply_kind(self):
        """
        Must belong to the same topic
        - TODO@ A post can reply to a post.
        """
        return []

    def save(self):
        """
        Overwrite save method to add to Elasticsearch.
        """

        # TODO should we validate the save worked before going to ES?

        from models.topic import Topic
        from models.user import User

        data = json_prep(self.deliver())
        topic = Topic.get(id=self['topic_id'])
        if topic:
            data['topic'] = json_prep(topic.deliver())
        user = User.get(id=self['user_id'])
        if user:
            data['user'] = json_prep(user.deliver())

        es.index(
            index='entity',
            doc_type='post',
            body=data,
            id=self['id'],
        )
        return super().save()
