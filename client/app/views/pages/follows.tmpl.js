const { div, h1, p, a, ul, li } = require('../../helpers/tags')
// const c = require('../../helpers/content').get
// const spinner = require('../components/spinner.tmpl')
const icon = require('../components/icon.tmpl')
const { copy } = require('../../helpers/utilities')
const previewSubjectHead = require('../components/preview_subject_head.tmpl')
const previewUnitHead = require('../components/preview_unit_head.tmpl')
const previewCardHead = require('../components/preview_card_head.tmpl')
const spinner = require('../components/spinner.tmpl')
const { getIsLoggedIn } = require('../../selectors/base')
const { goLogin } = require('../../helpers/auxiliaries')

const follow = data => {
  const kind = data.entity_kind
  const { name, body } = data.entityFull
  return li(
    { className: 'follow' },
    a(
      {
        id: data.id,
        href: '#',
        className: 'follows__unfollow-button',
      },
      icon('remove'),
      ' Unfollow'
    ),
    kind === 'unit'
      ? previewUnitHead({ name, body, labelKind: true })
      : kind === 'subject'
        ? previewSubjectHead({ name, body, labelKind: true })
        : kind === 'card'
          ? previewCardHead({
              name,
              kind: data.entityFull.kind,
              labelKind: true,
            })
          : kind === 'topic' ? 'A topic' : null
  )
}

const follows = data => {
  if (data.length) {
    return ul(data.map(f => follow(f)))
  }
  return p('No follows. ', a({ href: '/search' }, icon('search'), ' Search'))
}

module.exports = data => {
  if (getIsLoggedIn(data) === null) {
    return spinner()
  }

  if (!getIsLoggedIn(data)) {
    return goLogin()
  }
  // TODO-2 update this to look for some status field
  // if(!data.follows) { return spinner() }

  return div(
    { id: 'follows', className: 'page' },
    h1('Follows'),
    a({ href: '/notices' }, icon('back'), ' Back to notices.'),
    follows(
      data.follows.map(dfollow => {
        const ofKinds = data[`${dfollow.entity_kind}s`] || {}
        const entity = ofKinds[dfollow.entity_id]
        dfollow = copy(dfollow)
        dfollow.entityFull = entity || {}
        return dfollow
      })
    )
  )
}
