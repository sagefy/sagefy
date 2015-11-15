{a, i, h2, ul, li, span, p} = require('../../modules/tags')
{timeAgo, ucfirst} = require('../../modules/auxiliaries')

module.exports = (kind, entityID, topics) ->
    return [
        a(
            {
                className: 'font-size-small pull-right'
                href: "/topics/create?kind=unit&id=#{entityID}"
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
            ) for topic in topics
        ) if topics?.length
        p(
            'No topics yet.'
        ) unless topics?.length
        p(a(
            {href: "/search?kind=topic&q=#{entityID}"}
            'See more topics '
            i({className: 'fa fa-chevron-right'})
        ))
    ]
