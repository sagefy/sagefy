const {div, span} = require('../../modules/tags')
const {ucfirst} = require('../../modules/utilities')
const icon = require('./icon.tmpl')
const {previewName} = require('./preview_shared.fn')

module.exports = function previewCardHead({name, kind, url = false}) {
    return div(
        {className: 'preview--card__head'},
        previewName(name, 'card', url),
        kind ? span(
            {className: 'preview--card__kind'},
            icon(kind.toLowerCase()),
            ucfirst(kind)
        ) : null
    )
}
