from modules.model import Model
from modules.validations import is_required, is_string, is_entity_dict
from flask import g
import rethinkdb as r


class Topic(Model):
    """
    A discussion topic.

    A topic must be created along with a post.
    No topic should have no posts.
    """

    tablename = 'topics'

    schema = dict(Model.schema.copy(), **{
        'user_id': {
            'validate': (is_required, is_string,)
        },
        'name': {
            'validate': (is_required, is_string,)
        },
        'entity': {
            'validate': (is_required, is_entity_dict,)
        }
    })

    @classmethod
    def list_by_entity_id(cls, entity_id, limit=10, **params):
        """
        Get a list of models matching the provided keyword arguments.
        Return empty array when no models match.
        """

        data_list = (cls.table
                        .filter(lambda topic:
                                topic['entity']['id'] == entity_id)
                        .limit(10)
                        .order_by(r.desc('created'))
                        .run(g.db_conn))
        return [cls(data) for data in data_list]

    # TODO@ On create or update, update index in Elasticsearch
