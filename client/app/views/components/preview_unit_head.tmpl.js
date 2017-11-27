const { div, p } = require('../../modules/tags')
const { previewName } = require('./preview_shared.fn')

module.exports = function previewUnitHead({
  name,
  body,
  url = false,
  labelKind = false,
}) {
  return div(
    { className: 'preview--unit__head' },
    previewName({ name, kind: 'unit', url, labelKind }),
    body ? p(body) : null
  )
}
