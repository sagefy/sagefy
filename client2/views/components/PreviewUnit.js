/*

const { div } = require('../../helpers/tags')
const previewUnitHead = require('./preview_unit_head.tmpl')
const previewUnitContent = require('./preview_unit_content.tmpl')

module.exports = function previewUnit(data) {
  return div(
    { className: 'preview--unit' },
    previewUnitHead(data),
    previewUnitContent(data)
  )
}




const { div } = require('../../helpers/tags')
const {
  previewCommon,
  previewRequires,
  previewTags,
} = require('./preview_shared.fn')

// TODO-2 show diff option

module.exports = function previewUnitContent({
  status,
  available,
  created,
  language,
  requires,
  tags,
}) {
  return div(
    { className: 'preview--unit__content' },
    previewCommon({ created, status, available, language }),
    previewRequires(requires),
    previewTags(tags)
  )
}






const { div, p } = require('../../helpers/tags')
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


*/
