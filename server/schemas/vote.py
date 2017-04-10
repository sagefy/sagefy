from schemas.post import schema as post_schema
from modules.validations import is_required, is_string, is_boolean
from modules.util import extend


# For votes, a body is not required but optional,
# But a replies to id is required

schema = extend({}, post_schema, {
    'fields': {
        # The only true unique field of a vote...
        # Where True is yes, False is no
        'response': {
            'validate': (is_required, is_boolean,),
        }
    },
})

# A vote does not require a body
schema['fields']['body'] = {
    'validate': (is_string,)
}

# But a vote does require a proposal
schema['fields']['replies_to_id'] = {
    'validate': (is_required, is_string,)
}
