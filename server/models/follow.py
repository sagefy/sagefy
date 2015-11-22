from modules.model import Model
from modules.validations import is_required, is_string, is_one_of
import rethinkdb as r
import framework.database as database


class Follow(Model):
    """A following of an entity, topic, or proposal."""
    tablename = 'follows'

    schema = dict(Model.schema.copy(), **{
        'user_id': {
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
                        is_one_of, 'card', 'unit', 'set', 'topic'
                    )),
                }
            }
        }
    })

    @classmethod
    def list(cls, user_id=None, limit=10, skip=0,
             kind=None, entity_id=None, **params):
        """
        Get a list of models matching the provided arguments.
        Also adds pagination capabilities.
        Returns empty array when no models match.
        """

        query = (cls.table
                    .order_by(r.desc('created'))
                    .filter(r.row['user_id'] == user_id
                            if user_id is not None else True)
                    .filter(r.row['entity']['kind'] == kind
                            if kind is not None else True)
                    .filter(r.row['entity']['id'] == entity_id
                            if entity_id is not None else True)
                    .skip(skip)
                    .limit(limit))
        fields_list = query.run(database.db_conn)
        return [cls(fields) for fields in fields_list]
