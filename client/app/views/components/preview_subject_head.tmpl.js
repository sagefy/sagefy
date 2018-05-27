const { div, p } = require('../../helpers/tags')
const { previewName } = require('./preview_shared.fn')

module.exports = function previewSubjectHead({
  name,
  body,
  url = false,
  labelKind = false,
}) {
  return div(
    { className: 'preview--subject__head' },
    previewName({ name, kind: 'subject', url, labelKind }),
    body ? p(body) : null
  )
}
