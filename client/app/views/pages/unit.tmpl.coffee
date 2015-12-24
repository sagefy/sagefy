{div, h1, ul, li, span, header, p, h2, a, i} = require('../../modules/tags')
c = require('../../modules/content').get

followButton = require('../components/follow_button.tmpl')
entityHeader = require('../components/entity_header.tmpl')
entityTopics = require('../components/entity_topics.tmpl')
entityVersions = require('../components/entity_versions.tmpl')
entityRelationships = require('../components/entity_relationships.tmpl')

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

        ul(
            li("Language: #{c(unit.language)}")
            li("Tags: #{unit.tags.join(', ')}")
        )

        h2('Stats')
        ul(
            li('Number of Learners: ???')
            li('Quality: ???')
            li('Difficulty: ???')
        )

        entityRelationships('unit', unit)
        entityTopics('unit', unit.entity_id, unit.topics)
        entityVersions('unit', unit.entity_id, unit.versions)
    )
