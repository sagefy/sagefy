const { div, ul, li, a, input } = require('../../modules/tags')
const icon = require('./icon.tmpl')
const previewCardHead = require('./preview_card_head.tmpl')
const previewUnitHead = require('./preview_unit_head.tmpl')
const previewSubjectHead = require('./preview_subject_head.tmpl')

module.exports = (data) => {
    const entities = data.value || data.default || []
    return div(
        entities.length ? ul(
            { className: 'form-field--entities__ul' },
            entities.map((entity, index) => li(
                a(
                    {
                        id: entity.id,
                        href: '#',
                        className: 'form-field--entities__remove'
                    },
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
                entity.kind === 'subject' ?
                    previewSubjectHead({
                        name: entity.name,
                        body: entity.body,
                    }) :
                    null,
                Object.keys(entity).map(key => input({
                    type: 'hidden',
                    name: `${data.name}.${index}.${key}`,
                    value: entity[key],
                }))
            ))
        ) : null,
        data.add ? a(
            { className: 'form-field--entities__a', href: data.add.url },
            icon('search'),
            ` ${data.add.label}`
        ) : null
    )
}
