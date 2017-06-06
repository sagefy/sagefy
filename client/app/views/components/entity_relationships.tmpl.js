const { h2, ul, li, a } = require('../../modules/tags')

const verbage = {
    requires: 'Requires',
    required_by: 'Required by',
    belongs_to: 'Belongs to',
}

// const order = ['card', 'unit', 'subject']

module.exports = (kind, entity) => {
    return [
        h2('Relationships'),
        ul(
            entity.relationships.map(relation => {
                kind = findKind(kind, relation.kind)
                return li(
                    verbage[relation.kind],
                    ': ',
                    a(
                        { href: `/${kind}s/${relation.entity.entity_id}` },
                        relation.entity.name
                    )
                )
            })
        ),
    ]
}

const findKind = (curr, rel) => {
    if (rel === 'belongs_to') {
        if (curr === 'unit') {
            return 'subject'
        }

        if (curr === 'card') {
            return 'unit'
        }
    }

    return curr
}
