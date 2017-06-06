const { div, ul, li, a, h4, span } = require('../../modules/tags')
const { previewCommon, previewTags } =
    require('./preview_shared.fn')
const icon = require('./icon.tmpl')
const { ucfirst } = require('../../modules/auxiliaries')


// TODO-2 show diff option

module.exports = function previewSubjectContent({
    status,
    available,
    created,
    language,
    members,  // units and subjects: kind url name id
    units,  // just a list of units: url name id
    tags,
}) {
    return div(
        { className: 'preview--subject__content' },
        previewCommon({ created, status, available, language }),
        units && units.length ? [
            h4('List of Units'),
            ul(units.map(unit => li(
              unit.url ?
                  a({ href: unit.url }, unit.name || unit.id)
                  : unit.name || unit.id
            )))
        ] : null,
        members && members.length ? [
            h4('List of Members'),
            ul(
                { className: 'preview--subject__content__members' },
                members.map(member => li(
                member.kind ?
                    [span(
                        { className: 'preview--subject__content__members__kind' },
                        icon(member.kind), ` ${ucfirst(member.kind)}`
                    ), ' '] :
                    null,
                member.url ?
                    a({ href: member.url }, member.name || member.id)
                    : member.name || member.id
            )))
        ] : null,
        previewTags(tags)
    )
}
