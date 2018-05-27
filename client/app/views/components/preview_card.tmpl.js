const { div } = require('../../helpers/tags')
const previewCardHead = require('./preview_card_head.tmpl')
const previewCardContent = require('./preview_card_content.tmpl')

module.exports = function previewCard(data) {
  return div(
    { className: 'preview--card' },
    previewCardHead(data),
    previewCardContent(data)
  )
}
