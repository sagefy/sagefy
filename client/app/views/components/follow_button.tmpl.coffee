{a, i, p} = require('../../modules/tags')
icon = require('./icon.tmpl')

module.exports = (kind, entity_id, follows) ->
    following = follows?.find((f) -> f.entity.id is entity_id)
    return [
        a(
            {
                id: "#{kind}_#{entity_id}"
                href: '#'
                className: 'follow-button'
            }
            icon('follow')
            ' Follow'
        ) if not following
        p(
            {className: 'follow-button__following'}
            icon('follow')
            ' Following'
        ) if following
    ]
