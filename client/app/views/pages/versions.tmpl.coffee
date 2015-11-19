{div, h1, ul, li, span, strong, br, p, a, i} = require('../../modules/tags')
c = require('../../modules/content').get
{timeAgo, ucfirst} = require('../../modules/auxiliaries')

labelClasses = {
    pending: 'label'
    blocked: 'label--bad'
    declined: 'label'
    accepted: 'label--good'
}

module.exports = (data) ->
    [kind, id] = data.routeArgs

    versions = data["#{kind}Versions"]?[id]

    return div({className: 'spinner'}) unless versions

    latestAccepted = versions.find((v) -> v.status is 'accepted')

    return div(
        {id: 'versions', className: 'col-10'}
        h1("Versions: #{latestAccepted.name}")
        p(
            {className: 'leading'}
            a(
                {href: "/#{kind}s/#{id}"}
                i({className: 'fa fa-chevron-left'})
                " See #{kind} page"
            )
        )
        ul(
            li(row(kind, version)) for version in versions
        )
    )

    # TODO paginate

row = (kind, version) ->
    return [
        # Created ago
        span({className: 'timeago'}, timeAgo(version.created))
        # Status
        span(
            {className: 'status ' + labelClasses[version.status]}
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
            then span({className: 'avail label--bad'}, 'Hidden')

        # Language
        span({className: 'language'}, c(version.language))

        # Tags
        'Tags: ' + version.tags.join(', ')
    ]
