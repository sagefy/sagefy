const {div, p} = require('../../modules/tags')
const {previewName} = require('./preview_shared.fn')

module.exports = function previewSetHead({name, body, url = false}) {
    return div(
        {className: 'preview--set__head'},
        previewName(name, 'set', url),
        body ? p(body) : null
    )
}
