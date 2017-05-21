from schemas.index import schema as default
from modules.util import extend
from modules.validations import is_required, is_language, is_boolean, \
    is_list, is_string, is_list_of_strings, is_one_of, has_min_length
from modules.util import uniqid


"""
The model represents a **version** of an entity, not an entity itself.
The `entity_id` attribute is what refers to a particular entity.
The `id` attribute refers to a specific version of the entity.
The `previous_id` attribute refers to the version based off.
"""

schema = extend({}, default, {
    'fields': {
        'entity_id': {
            'validate': (is_required, is_string,),
            'default': uniqid
        },
        'previous_id': {  # TODO-2 is valid id? (set by code)
            'validate': (is_string,),
        },
        'language': {
            'validate': (is_required, is_language,),
            'default': 'en'
        },
        'name': {
            'validate': (is_required, is_string, (has_min_length, 1),)
        },
        'status': {
            'validate': (is_required, (
                is_one_of, 'pending', 'blocked', 'accepted', 'declined'
            )),
            'default': 'pending'
        },
        'available': {
            'validate': (is_boolean,),
            'default': True
        },
        'tags': {
            'validate': (is_list, is_list_of_strings),
            'default': []
        },
    },
})
