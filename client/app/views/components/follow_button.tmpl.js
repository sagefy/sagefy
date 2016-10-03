const {a, p} = require('../../modules/tags')
const icon = require('./icon.tmpl')

module.exports = (kind, entity_id, follows) => {
    const following = follows && follows.find((f) => f.entity.id === entity_id)
    return following ? p(
        {className: 'follow-button__following'},
        icon('follow'),
        ' Following'
    ) : a(
        {
            id: `${kind}_${entity_id}`,
            href: '#',
            className: 'follow-button',
        },
        icon('follow'),
        ' Follow'
    )
}
