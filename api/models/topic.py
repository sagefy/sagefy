from modules.model import Model
from modules.validations import is_required, is_string, is_entity_dict


class Topic(Model):
    """A discussion topic."""
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

    # A topic must be created along with a post. No topic should have no posts.
