from modules.model import Model
from modules.validations import is_required, is_string, is_list_of_strings
from models.set import Set


class UserSets(Model):
    """
    Record the list of sets the learner has added.
    """

    tablename = 'users_sets'

    schema = dict(Model.schema.copy(), **{
        'user_id': {  # TODO-2 validate foreign
            'validate': (is_required, is_string,),
        },
        'set_ids': {
            'validate': (is_required, is_list_of_strings,),
        }
    })

    def list_sets(self, db_conn, limit=10, skip=0, **params):
        """
        Join the user's set_ids with set information.
        Return empty list when there's no matching documents.
        """

        return Set.list_by_entity_ids(db_conn, self['set_ids'])

        # TODO-2 each set -- needs review?
        # TODO-2 order by last reviewed time
        # TODO-2 pagination
