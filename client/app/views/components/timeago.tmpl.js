const { span } = require('../../helpers/tags')
const { timeAgo } = require('../../helpers/auxiliaries')

module.exports = (time, { right } = {}) =>
  span(
    {
      className: `timeago${right ? ' timeago--right' : ''}`,
    },
    timeAgo(time)
  )
