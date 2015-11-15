{h2, ul, li, a} = require('../../modules/tags')

verbage = {
    requires: 'Requires'
    required_by: 'Required by'
    belongs_to: 'Belongs to'
}

order = ['card', 'unit', 'set']

module.exports = (kind, entity) ->
    return [
        h2('Relationships')
        ul(
            for relation in entity.relationships
                kind = findKind(kind, relation.kind)
                li(
                    verbage[relation.kind]
                    ': '
                    a(
                        {href: "/#{kind}s/#{relation.entity.id}"}
                        relation.entity.name
                    )
                )
        )
    ]

findKind = (curr, rel) ->
    if rel is 'belongs_to'
        if curr is 'unit'
            return 'set'

        if curr is 'card'
            return 'unit'

    return curr
