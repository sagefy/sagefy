const { div } = require('../../helpers/tags')
const previewSubjectHead = require('./preview_subject_head.tmpl')
const previewSubjectContent = require('./preview_subject_content.tmpl')

module.exports = function previewSubject(data) {
  return div(
    { className: 'preview--subject' },
    previewSubjectHead(data),
    previewSubjectContent(data)
  )
}
