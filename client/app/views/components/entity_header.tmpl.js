const { header, span, h1 } = require('../../helpers/tags')
const { titleize } = require('../../helpers/auxiliaries')
const icon = require('./icon.tmpl')

module.exports = (kind, entity) => {
  let title = titleize(kind)
  if (kind === 'card') {
    title = `${titleize(entity.kind)} ${title}`
  }

  return header(
    { className: 'entity-header' },
    span({ className: 'entity-header__kind' }, icon(kind), ` ${title}`),
    h1(entity.name)
  )
}
