const { div, span } = require('../../modules/tags')
const { ucfirst } = require('../../modules/auxiliaries')
const icon = require('./icon.tmpl')
const { previewName } = require('./preview_shared.fn')

module.exports = function previewCardHead({
    name,
    kind,
    url = false,
    labelKind = false,
}) {
    const cardKindLabel = kind ? span(
        { className: 'preview--card__kind' },
        icon(kind.toLowerCase()),
        ucfirst(kind)
    ) : null
    return div(
        { className: 'preview--card__head' },
        previewName({
            name: [cardKindLabel, ' ', name],
            kind: 'card',
            url,
            labelKind
        })
    )
}
