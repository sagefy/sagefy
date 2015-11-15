{div, h1, ul, li, span, header, p, h2, a, i} = require('../../modules/tags')
c = require('../../modules/content').get

followButton = require('../components/follow_button.tmpl')
entityHeader = require('../components/entity_header.tmpl')
entityTopics = require('../components/entity_topics.tmpl')
entityVersions = require('../components/entity_versions.tmpl')

verbage = {
    requires: 'Requires'
    required_by: 'Required by'
    belongs_to: 'Belongs to'
}


module.exports = (data) ->
    id = data.routeArgs[0]
    unit = data.units?[id]

    return div({className: 'spinner'}) unless unit

    return div(
        {id: 'unit', className: 'col-8 entity-page'}

        # TODO Flag button
        followButton('unit', unit.entity_id, data.follows)
        entityHeader('unit', unit)

        p({className: 'leading'}, unit.body)

        h2('Stats')
        ul(
            li('Number of Learners: ???')
            li('Quality: ???')
            li('Difficulty: ???')
        )

        h2('Relationships')
        ul(
            for relation in unit.relationships
                kind = if relation.kind is 'belongs_to' then 'set' else 'unit'
                li(
                    verbage[relation.kind]
                    ': '
                    a(
                        {href: "/#{kind}s/#{relation.entity.id}"}
                        relation.entity.name
                    )
                )
        )

        entityTopics('unit', unit.entity_id, unit.topics)
        entityVersions('unit', unit.entity_id, unit.versions)
    )
