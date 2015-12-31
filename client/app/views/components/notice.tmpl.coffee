{li, span} = require('../../modules/tags')
timeAgo = require('../../modules/auxiliaries').timeAgo

# TODO-2 add a link around the notice, and go to the appropriate page on click.

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
