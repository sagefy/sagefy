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
            'validate': (is_string,)
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

        es.index(
            index='entity',
            doc_type='post',
            body=json_prep(self.deliver()),
            id=self['id'],
        )
        return super().save()
