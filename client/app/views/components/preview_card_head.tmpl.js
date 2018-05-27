const { div } = require('../../helpers/tags')
const { previewName } = require('./preview_shared.fn')

module.exports = function previewCardHead({
  name,
  kind,
  url = false,
  labelKind = false,
}) {
  return div(
    { className: 'preview--card__head' },
    previewName({
      name,
      kind: 'card',
      url,
      labelKind,
      cardKindLabel: kind,
    })
  )
}
