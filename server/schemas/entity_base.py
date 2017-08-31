from schemas.index import schema as default
from modules.util import extend

"""
The model represents a **version** of an entity, not an entity itself.
The `entity_id` attribute is what refers to a particular entity.
The `id` attribute refers to a specific version of the entity.
The `previous_id` attribute refers to the version based off.
"""

schema = extend({}, default, {
    'fields': {
        'entity_id': {},
        'previous_id': {},
        'language': {},
        'name': {},
        'status': {},
        'available': {},
        'tags': {},
        'user_id': {},
    },
})
