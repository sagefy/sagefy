{div, h1, ul, li, span, strong, br, p, a, i} = require('../../modules/tags')
c = require('../../modules/content').get
{timeAgo, ucfirst} = require('../../modules/auxiliaries')
spinner = require('../components/spinner.tmpl')
timeago = require('../components/timeago.tmpl')
icon = require('../components/icon.tmpl')

# TODO-2 Version history and proposal view should have the same layout,
#        and be similar to the page

module.exports = (data) ->
    [kind, id] = data.routeArgs

    versions = data["#{kind}Versions"]?[id]

    return spinner() unless versions

    latestAccepted = versions.find((v) -> v.status is 'accepted')

    return div(
        {id: 'versions'}
        h1("Versions: #{latestAccepted.name}")
        p(
            a(
                {href: "/#{kind}s/#{id}"}
                icon('back')
                " See #{kind} page"
            )
        )
        ul(
            li(row(kind, version)) for version in versions
        )
    )

    # TODO-2 paginate

row = (kind, version) ->
    return [
        # Created ago
        timeago(version.created, {right: true})
        # Status
        span(
            {className: 'versions__status--' + version.status}
            ucfirst(version.status)
        )
        # Name
        strong(version.name)

        br()

        # Contents
        if kind is 'card'
            [
                "#{ucfirst(version.kind)}; "
                "Unit: #{version.unit_id}; "
                "Requires: #{version.require_ids.join(', ') or 'None'}; "
                if version.kind is 'video'
                    "#{version.site}: #{version.video_id}; "
                else if version.kind is 'choice'
                    [
                        "Body: #{version.body}"
                        br()
                        "Options: #{JSON.stringify(version.options)}"
                        br()
                        "Order: #{version.order}; "
                        "Max options to show: #{version.max_options_to_show}"
                    ]
            ]
        else if kind is 'unit'
            [
                version.body
                br()
                "Requires: #{version.require_ids.join(', ') or 'None'}"
            ]
        else if kind is 'set'
            [
                version.body
                br()
                "#{ucfirst(member.kind)}: #{member.id}; " \
                    for member in version.members
            ]

        br()

        # Available
        if not version.available \
            then span({className: 'avail'}, 'Hidden')

        # Language
        span({className: 'language'}, c(version.language))

        # Tags
        'Tags: ' + version.tags.join(', ')
    ]
