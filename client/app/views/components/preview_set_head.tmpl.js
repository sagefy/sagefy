const {div, p} = require('../../modules/tags')
const {previewName} = require('./preview_shared.fn')

module.exports = function previewSetHead({
    name,
    body,
    url = false,
    labelKind = false,
}) {
    return div(
        {className: 'preview--set__head'},
        previewName({name, kind: 'set', url, labelKind}),
        body ? p(body) : null
    )
}
