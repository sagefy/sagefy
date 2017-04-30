const {div, ul, li, a, input} = require('../../modules/tags')
const icon = require('./icon.tmpl')
const previewCardHead = require('./preview_card_head.tmpl')
const previewUnitHead = require('./preview_unit_head.tmpl')
const previewSetHead = require('./preview_set_head.tmpl')

module.exports = (data) => {
    const entities = data.value || data.default || []
    return div(
        entities.length ? ul(
            {className: 'form-field--entities__ul'},
            entities.map((entity, index) => li(
                a(
                    {href: '#', className: 'form-field--entities__remove'},
                    icon('remove'),
                    ' Remove'
                ),
                entity.kind === 'card' ?
                    previewCardHead({
                        name: entity.name,
                        kind: entity.kind,
                    }) :
                entity.kind === 'unit' ?
                    previewUnitHead({
                        name: entity.name,
                        body: entity.body,
                    }) :
                entity.kind === 'set' ?
                    previewSetHead({
                        name: entity.name,
                        body: entity.body,
                    }) :
                    null,
                input({
                    type: 'hidden',
                    name: `members.${index}.kind`,
                    value: entity.kind,
                }),
                input({
                    type: 'hidden',
                    name: `members.${index}.id`,
                    value: entity.id,
                })
            ))
        ) : null,
        data.add ? a(
            {className: 'form-field--entities__a', href: data.add.url},
            icon('search'),
            ` ${data.add.label}`
        ) : null
    )
}
