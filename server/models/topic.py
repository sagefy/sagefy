from modules.model import Model
from modules.validations import is_required, is_string, is_one_of, \
    has_min_length
from modules.util import json_prep
import rethinkdb as r
from framework.elasticsearch import es


class Topic(Model):
    """
    A discussion topic.

    A topic must be created along with a post.
    No topic should have no posts.
    """

    tablename = 'topics'

    schema = dict(Model.schema.copy(), **{
        'user_id': {  # TODO-2 validate foreign
            'validate': (is_required, is_string,)
        },
        'name': {
            'validate': (is_required, is_string, (has_min_length, 1),)
        },
        'entity': {
            'validate': (is_required,),
            'embed': {
                'id': {  # TODO-0 validate foreign
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
    def list_by_entity_id(cls, db_conn, entity_id, limit=10, skip=0, **params):
        """
        Get a list of models matching the provided keyword arguments.
        Return empty array when no models match.
        """

        data_list = (cls.table
                        .filter(r.row['entity']['id'] == entity_id)
                        .order_by(r.desc('created'))
                        .limit(limit)
                        .skip(skip)
                        .run(db_conn))
        documents = [cls(data) for data in data_list]
        return documents

    def save(self, db_conn):
        """
        Overwrite save method to add to Elasticsearch.
        """

        # TODO-2 should we validate the save worked before going to ES?

        es.index(
            index='entity',
            doc_type='topic',
            body=json_prep(self.deliver()),
            id=self['id'],
        )
        return super().save(db_conn)
