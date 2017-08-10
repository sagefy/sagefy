const { span } = require('../../modules/tags')
const { timeAgo } = require('../../modules/auxiliaries')

module.exports = (time, { right } = {}) =>
    span(
        {
            className: `timeago${right ? ' timeago--right' : ''}`,
        },
        timeAgo(time)
    )
