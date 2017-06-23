const { div } = require('../../modules/tags')
const previewUnitHead = require('./preview_unit_head.tmpl')
const previewUnitContent = require('./preview_unit_content.tmpl')

module.exports = function previewUnit(data) {
    return div(
        { className: 'preview--unit' },
        previewUnitHead(data),
        previewUnitContent(data)
    )
}
