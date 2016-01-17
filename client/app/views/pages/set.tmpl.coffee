{div, h1, p, h2, ul, li, a, i} = require('../../modules/tags')
c = require('../../modules/content').get
followButton = require('../components/follow_button.tmpl')
entityHeader = require('../components/entity_header.tmpl')
entityTopics = require('../components/entity_topics.tmpl')
entityVersions = require('../components/entity_versions.tmpl')
spinner = require('../components/spinner.tmpl')


module.exports = (data) ->
    id = data.routeArgs[0]
    set = data.sets?[id]

    return spinner() unless set

    following = data.follows?.find((f) -> f.entity.id is set.entity_id)

    return div(
        {id: 'set'}

        followButton('set', set.entity_id, data.follows)
        entityHeader('set', set)

        p(set.body)

        ul(
            li("Language: #{c(set.language)}")
            li("Tags: #{set.tags.join(', ')}")
        )

        h2('Stats')
        ul(
            li('Number of Learners: ???')
            li('Quality: ???')
            li('Difficulty: ???')
        )

        h2({className: 'set__list-units-h2'}, 'List of Units')
        a(
            {href: "/sets/#{set.entity_id}/tree"}
            i({className: 'fa fa-tree'})
            ' View Tree'
        )
        ul(
            li(a(
                {href: "/units/#{unit.entity_id}"}
                unit.name
            )) for unit in set.units
        )

        entityTopics('set', set.entity_id, set.topics)
        entityVersions('set', set.entity_id, set.versions)
    )
