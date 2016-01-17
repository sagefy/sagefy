{span} = require('../../modules/tags')
{timeAgo} = require('../../modules/auxiliaries')

module.exports = (time, {right} = {}) ->
    return span(
        {
            className: 'timeago' + (
                if right
                then ' timeago--right'
                else ''
            )
        }
        timeAgo(time)
    )
