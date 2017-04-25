const {div, ul, li, a} = require('../../modules/tags')
const {previewCommon, previewTags} =
    require('./preview_shared.fn')
const icon = require('./icon.tmpl')
const {ucfirst} = require('../../modules/utilities')


// TODO-2 show diff option

module.exports = function previewSetContent({
    status,
    available,
    created,
    language,
    members,  // units and sets: kind url name id
    units,  // just a list of units: url name id
    tags,
}) {
    return div(
        {className: 'preview--set__content'},
        previewCommon({created, status, available, language}),
        members && members.length ? ul(members.map(member => li(
          member.kind ? [icon(member.kind), ` ${ucfirst(member.kind)}`] : null,
          member.url ?
              a({href: member.url}, member.name || member.id)
              : member.name || member.id
        ))) : null,
        units && units.length ? ul(units.map(unit => li(
          unit.url ?
              a({href: unit.url}, unit.name || unit.id)
              : unit.name || unit.id
        ))) : null,
        previewTags(tags)
    )
}
