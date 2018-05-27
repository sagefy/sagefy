const { div, h1, ul, li, p, a } = require('../../helpers/tags')
const spinner = require('../components/spinner.tmpl')
const icon = require('../components/icon.tmpl')

const previewCard = require('../components/preview_card.tmpl')
const previewUnit = require('../components/preview_unit.tmpl')
const previewSubject = require('../components/preview_subject.tmpl')

// TODO-2 Version history and proposal view should have the same layout,
//    and be similar to the page

const row = (kind, version) => {
  if (kind === 'card') {
    return previewCard(
      Object.assign({}, version, {
        unit: { name: version.unit_id },
        requires: version.require_ids.map(id => ({ id })),
      })
    )
  }

  if (kind === 'unit') {
    return previewUnit(
      Object.assign({}, version, {
        requires: version.require_ids.map(id => ({ id })),
      })
    )
  }

  if (kind === 'subject') {
    return previewSubject(version)
  }

  return null
  /* [

    // Contents
    ] : kind === 'unit' ? [
      `Requires: ${version.require_ids.join(', ') || 'None'}`
    ] :

  ] */
}

module.exports = data => {
  const [kind, id] = data.routeArgs
  const versions = data[`${kind}Versions`] && data[`${kind}Versions`][id]
  if (!versions) {
    return spinner()
  }
  const latestAccepted = versions.find(v => v.status === 'accepted')

  return div(
    { id: 'versions', className: 'page' },
    h1(`Versions: ${latestAccepted.name}`),
    p(a({ href: `/${kind}s/${id}` }, icon('back'), ` See ${kind} page`)),
    ul(versions.map(version => li(row(kind, version))))
  )

  // TODO-2 paginate
}
