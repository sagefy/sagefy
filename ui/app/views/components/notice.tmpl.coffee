{li, span} = require('../../modules/tags')
timeAgo = require('../../modules/auxiliaries').timeAgo

module.exports = (data) ->
    return li(
        {
            className: if data.read then 'notice' else 'notice notice--unread'
            id: data.id
        }
        span(
            {className: 'notice__when'}
            timeAgo(data.created)
        )
        data.body
    )
