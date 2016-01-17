{h2, ul, li, span, p, a, i} = require('../../modules/tags')
{timeAgo, ucfirst} = require('../../modules/auxiliaries')
timeago = require('./timeago.tmpl')

module.exports = (kind, entityID, versions) ->
    return [
        h2('Versions')
        ul(
            {className: 'entity-versions'}
            li(
                timeago(version.created, {right: true})
                span(
                    {className: 'entity-versions__status--' + version.status}
                    ucfirst(version.status)
                )
                ' '
                version.name
            ) for version in versions
            li(
                a(
                    {href: "/#{kind}s/#{entityID}/versions"}
                    '... See more version history '
                    i({className: 'fa fa-chevron-right'})
                )
            )
        )
    ]
