from modules.model import Model
from modules.validations import is_required, is_string, is_number
from modules.content import get as c
import rethinkdb as r
import framework.database as database


def is_score(val):
    if val > 1 or val < 0:
        return c('number')


class Response(Model):
    """
    Record the list of sets the learner has added.
    """
    tablename = 'responses'

    schema = dict(Model.schema.copy(), **{
        'user_id': {
            'validate': (is_required, is_string,),
        },
        'card_id': {
            'validate': (is_required, is_string,),
        },
        'unit_id': {
            'validate': (is_required, is_string,),
        },
        'response': {
            'validate': (is_required,)
        },
        'score': {
            'validate': (is_required, is_number, is_score,),
        },
        'learned': {
            'validate': (is_required, is_number,)
        }
    })

    @classmethod
    def get_latest(cls, user_id, unit_id):
        """
        Get the latest response given a user ID and a unit ID.
        """

        query = (cls.table
                    .filter(r.row['user_id'].eq(user_id))
                    .filter(r.row['unit_id'].eq(unit_id))
                    .max('created')
                    .default(None))
        document = query.run(database.db_conn)
        if document:
            return cls(document)
