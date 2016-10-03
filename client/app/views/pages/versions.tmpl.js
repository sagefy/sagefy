const {div, h1, ul, li, span, strong, br, p, a} = require('../../modules/tags')
const c = require('../../modules/content').get
const {ucfirst} = require('../../modules/auxiliaries')
const spinner = require('../components/spinner.tmpl')
const timeago = require('../components/timeago.tmpl')
const icon = require('../components/icon.tmpl')

// TODO-2 Version history and proposal view should have the same layout,
//        and be similar to the page

module.exports = (data) => {
    const [kind, id] = data.routeArgs
    const versions = data[`${kind}Versions`] && data[`${kind}Versions`][id]
    if(!versions) { return spinner() }
    const latestAccepted = versions.find((v) => v.status === 'accepted')

    return div(
        {id: 'versions'},
        h1(`Versions: ${latestAccepted.name}`),
        p(
            a(
                {href: `/${kind}s/${id}`},
                icon('back'),
                ` See ${kind} page`
            )
        ),
        ul(
            versions.map(version => li(row(kind, version)))
        )
    )

    // TODO-2 paginate
}

const row = (kind, version) =>
    [
        // Created ago
        timeago(version.created, {right: true}),
        // Status
        span(
            {className: 'versions__status--' + version.status},
            ucfirst(version.status)
        ),
        // Name
        strong(version.name),

        br(),

        // Contents
        kind === 'card' ? [
            `${ucfirst(version.kind)}; `,
            `Unit: ${version.unit_id}; `,
            `Requires: ${version.require_ids.join(', ') || 'None'}; `,
            version.kind === 'video' ?
                `${version.site}: ${version.video_id}; `
                : version.kind === 'choice' ?
                [
                    `Body: ${version.body}`,
                    br(),
                    `Options: ${JSON.stringify(version.options)}`,
                    br(),
                    `Order: ${version.order}; `,
                    `Max options to show: ${version.max_options_to_show}`
                ] :
                null
        ] : kind === 'unit' ? [
            version.body,
            br(),
            `Requires: ${version.require_ids.join(', ') || 'None'}`
        ] : kind === 'set' ? [
            version.body,
            br(),
            version.members.map(
                member => `${ucfirst(member.kind)}: ${member.id}; `
            )
        ] : null,

        br(),

        // Available
        version.available ? null : span({className: 'avail'}, 'Hidden'),

        // Language
        span({className: 'language'}, c(version.language)),

        // Tags
        'Tags: ' + version.tags.join(', '),
    ]
