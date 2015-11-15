{h2, ul, li, span, p, a, i} = require('../../modules/tags')
{timeAgo, ucfirst} = require('../../modules/auxiliaries')


labelClasses = {
    pending: 'label'
    blocked: 'label--bad'
    declined: 'label'
    accepted: 'label--good'
}


module.exports = (kind, entityID, versions) ->
    return [
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
            ) for version in versions
        )
        p(a(
            {href: "/units/#{entityID}/versions"}
            'See more version history '
            i({className: 'fa fa-chevron-right'})
        ))
    ]
