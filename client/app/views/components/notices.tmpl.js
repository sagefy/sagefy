const { ul, p } = require('../../helpers/tags')
const notice = require('./notice.tmpl')

module.exports = data => {
  if (!data.length) {
    return p('No notices.')
  }
  return ul({ className: 'notices' }, data.map(n => notice(n)))
  // TODO-2 request more notices
}
