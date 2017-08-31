from schemas.post import schema as post_schema
from schemas.post import is_valid_reply
from modules.validations import is_required, is_string, is_one_of, is_list, \
    has_min_length
from modules.util import extend


def validate_entity_versions(db_conn, schema, data):
    """
    Ensure all the entity versions exist.
    """

    for p_entity_version in data['entity_versions']:
        entity_kind = p_entity_version['kind']
        tablename = '%ss' % entity_kind
        version_id = p_entity_version['id']
        entity_version = get_version(db_conn, tablename, version_id)
        if not entity_version:
            return [{
                'name': 'entity_versions',
                'message': 'Not a valid version: {entity_kind} {version_id}'
                .format(
                    entity_kind=entity_kind,
                    version_id=version_id
                ),
            }]
    return []


schema = extend({}, post_schema, {
    'fields': {
        'entity_versions': {
            'validate': (is_list, (has_min_length, 1)),
            'embed_many': {
                'id': {
                    'validate': (is_required, is_string,),
                },
                'kind': {
                    'validate': (is_required, is_string, (
                        is_one_of, 'card', 'unit', 'subject',
                    )),
                }
            }
        },
    },
    'validate': (is_valid_reply, validate_entity_versions),
})
