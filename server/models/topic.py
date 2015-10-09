from modules.model import Model
from modules.validations import is_required, is_string, is_one_of
import framework.database as database
import rethinkdb as r


# TODO@ On create or update, update index in Elasticsearch
# http://bit.ly/1VxHoBv
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
            'validate': (is_required,),
            'embed': {
                'id': {
                    'validate': (is_required, is_string,),
                },
                'kind': {
                    'validate': (is_required, is_string, (
                        is_one_of, 'card', 'unit', 'set'
                    )),
                }
            }
        }
    })

    @classmethod
    def list_by_entity_id(cls, entity_id, limit=10, skip=0, **params):
        """
        Get a list of models matching the provided keyword arguments.
        Return empty array when no models match.
        """

        data_list = (cls.table
                        .filter(r.row['entity']['id'] == entity_id)
                        .order_by(r.desc('created'))
                        .limit(limit)
                        .skip(skip)
                        .run(database.db_conn))
        documents = [cls(data) for data in data_list]
        return documents
