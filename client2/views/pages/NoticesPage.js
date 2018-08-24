/*

const { div, h1, p, a } = require('../../helpers/tags')
const notices = require('../components/notices.tmpl')
const spinner = require('../components/spinner.tmpl')
const icon = require('../components/icon.tmpl')
const { getIsLoggedIn } = require('../../selectors/base')
const goLogin = require('../../helpers/go_login')

module.exports = data => {
  if (getIsLoggedIn(data) === null) {
    return spinner()
  }

  if (!getIsLoggedIn(data)) {
    return goLogin()
  }

  // TODO-2 update this to use a status field
  if (!data.notices) {
    return spinner()
  }

  return div(
    { id: 'notices', className: 'page' },
    h1('Notices'),
    p(a({ href: '/follows' }, icon('follow'), ' Manage what I follow')),
    notices(data.notices)
  )
}



const { ul, p } = require('../../helpers/tags')
const notice = require('./notice.tmpl')

module.exports = data => {
  if (!data.length) {
    return p('No notices.')
  }
  return ul({ className: 'notices' }, data.map(n => notice(n)))
  // TODO-2 request more notices
}

module.exports = (store, broker) => {
  const { getTasks } = store
  broker.add({
    'click .notice'(e, el) {
      if (el.classList.contains('notice--unread')) {
        getTasks().markNotice(el.id)
      }
    },
  })
}

const { li, span } = require('../../helpers/tags')
const timeago = require('./timeago.tmpl')

// TODO-2 add a link around the notice, and go to the appropriate page on click.

module.exports = data =>
  li(
    {
      className: data.read ? 'notice' : 'notice notice--unread',
      id: data.id,
    },
    span({ className: 'notice__when' }, timeago(data.created)),
    data.body
  )


*/
