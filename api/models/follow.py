from modules.model import Model
from modules.validations import is_required, is_string, is_entity_dict


class Follow(Model):
    """A following of an entity, topic, or proposal."""
    tablename = 'follows'

    schema = dict(Model.schema.copy(), **{
        'user_id': {
            'validate': (is_required, is_string,)
        },
        'entity': {
            'validate': (is_required, is_entity_dict,)
        }
    })
