const { h2, ul, li, span, a } = require('../../modules/tags')
const { ucfirst } = require('../../modules/auxiliaries')
const timeago = require('./timeago.tmpl')
const icon = require('./icon.tmpl')

module.exports = (kind, entityID, versions) => {
    return [
        h2('Versions'),
        ul(
            { className: 'entity-versions' },
            versions && versions.map(version => li(
                timeago(version.created, { right: true }),
                span(
                    { className: `entity-versions__status--${version.status}` },
                    ucfirst(version.status)
                ),
                ' ',
                version.name
            )),
            li(
                a(
                    { href: `/${kind}s/${entityID}/versions` },
                    '... See more version history ',
                    icon('next')
                )
            )
        ),
    ]
}
