const {div, ul, li, a} = require('../../modules/tags')
const icon = require('./icon.tmpl')
const previewCardHead = require('./preview_card_head.tmpl')
const previewUnitHead = require('./preview_unit_head.tmpl')
const previewSetHead = require('./preview_set_head.tmpl')

module.exports = (data) => {
    const entities = data.value || data.default || []
    return div(
        entities.length ? ul(
            {className: 'form-field--entities__ul'},
            entities.map(entity => li(
                entity.kind === 'card' ?
                    previewCardHead({}) :
                entity.kind === 'unit' ?
                    previewUnitHead({}) :
                entity.kind === 'set' ?
                    previewSetHead({}) :
                    null
            ))
        ) : null,
        data.add ? a(
            {className: 'form-field--entities__a', href: data.add.url},
            icon('search'),
            ` ${data.add.label}`
        ) : null
    )
}
