const {div} = require('../../modules/tags')
const previewSetHead = require('./preview_set_head.tmpl')
const previewSetContent = require('./preview_set_content.tmpl')

module.exports = function previewSet(data) {
    return div(
        {className: 'preview--set'},
        previewSetHead(data),
        previewSetContent(data)
    )
}
