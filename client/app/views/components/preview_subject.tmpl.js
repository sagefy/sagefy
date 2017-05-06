const {div} = require('../../modules/tags')
const previewSubjectHead = require('./preview_subject_head.tmpl')
const previewSubjectContent = require('./preview_subject_content.tmpl')

module.exports = function previewSubject(data) {
    return div(
        {className: 'preview--subject'},
        previewSubjectHead(data),
        previewSubjectContent(data)
    )
}
