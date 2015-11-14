{div, h1, ul, li, span, header, p, h2, a, i} = require('../../modules/tags')
c = require('../../modules/content').get
{timeAgo, ucfirst} = require('../../modules/auxiliaries')

labelClasses = {
    pending: 'label'
    blocked: 'label--bad'
    declined: 'label'
    accepted: 'label--good'
}

verbage = {
    requires: 'Requires'
    required_by: 'Required by'
    belongs_to: 'Belongs to'
}


module.exports = (data) ->
    id = data.routeArgs[0]
    unit = data.units?[id]

    return div({className: 'spinner'}) unless unit

    following = data.follows?.find((f) -> f.entity.id is unit.entity_id)

    return div(
        {id: 'unit', className: 'col-8'}

        a(
            {
                id: unit.entity_id
                href: '#'
                className: 'follow button button--good pull-right'
            }
            i({className: 'fa fa-heart'})
            ' Follow'
        ) if not following
        p(
            {className: 'label--good pull-right'}
            i({className: 'fa fa-check'})
            ' Following'
        ) if following
        # TODO Flag button

        header(
            span({className: 'label--accent font-size-accent'}, 'Unit')
            h1(unit.name)
            ul(
                li("Language: #{c(unit.language)}")
                li("Tags: #{unit.tags.join(', ')}")
            )
        )

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


        a(
            {
                className: 'font-size-small pull-right'
                href: "/topics/create?kind=unit&id=#{unit.entity_id}"
            }
            i({className: 'fa fa-plus'})
            ' Create a new topic'
        )
        h2('Topics')
        ul(
            li(
                span({className: 'timeago'}, timeAgo(topic.created))
                # TODO update time ago to latest post time
                a(
                    {href: "/topics/#{topic.id}"}
                    topic.name
                )
                # TODO number of posts
            ) for topic in unit.topics
        )
        p(a(
            {href: "/search?kind=topic&q=#{unit.entity_id}"}
            'See more topics '
            i({className: 'fa fa-chevron-right'})
        ))


        h2('Versions')
        ul(
            {className: 'versions'}
            li(
                span({className: 'timeago'}, timeAgo(version.created))
                span(
                    {className: labelClasses[version.status]}
                    ucfirst(version.status)
                )
                ' '
                version.name
            ) for version in unit.versions
        )
        p(a(
            {href: "/units/#{unit.entity_id}/versions"}
            'See more version history '
            i({className: 'fa fa-chevron-right'})
        ))
    )
