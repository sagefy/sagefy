const { li, span } = require('../../helpers/tags')
const { timeAgo } = require('../../helpers/auxiliaries')

// TODO-2 add a link around the notice, and go to the appropriate page on click.

module.exports = data =>
  li(
    {
      className: data.read ? 'notice' : 'notice notice--unread',
      id: data.id,
    },
    span({ className: 'notice__when' }, timeAgo(data.created)),
    data.body
  )
