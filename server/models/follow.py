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

    def validate(self):
        """
        Overwrite validate method to check options.
        """

        errors = super().validate()
        if not errors:
            errors = self.validate_uniqueness()
        return errors

    def validate_uniqueness(self):
        """
        Ensure the user is not already following the entity BEFORE insert.
        """

        prev = Follow.list(user_id=self['user_id'],
                           entity_id=self['entity']['id'])
        if prev:
            return [{'message': 'Already followed.'}]
        return []

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

    @classmethod
    def get_user_ids_by_entity(cls, entity_id, entity_kind):
        query = (cls.table
                    .filter(r.row['entity']['id'] == entity_id)
                    .filter(r.row['entity']['kind'] == entity_kind))
        fields_list = query.run(database.db_conn)
        return [fields['user_id'] for fields in fields_list]
