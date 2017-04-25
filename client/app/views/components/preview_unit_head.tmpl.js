const {div, p} = require('../../modules/tags')
const {previewName} = require('./preview_shared.fn')

module.exports = function previewUnitHead({name, body, url = false}) {
    return div(
        {className: 'preview--unit__head'},
        previewName(name, 'unit', url),
        body ? p(body) : null
    )
}
