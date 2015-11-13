{div, h1, p, img, figure, h3, header} = require('../../modules/tags')
{timeAgo} = require('../../modules/auxiliaries')

module.exports = (data) ->
    [id] = data.routeArgs
    user = data.users?[id]
    return div({className: 'spinner'}) unless user

    return div(
        {id: 'profile', className: 'col-6'}
        header(
            img({src: user.avatar, className: 'avatar'})
            h1(user.name)
            p({className: 'timeago'}, 'Joined ' + timeAgo(user.created))
        )
        h3("#{user.name} is learning:")
        # TODO sets - if available   and link to search
        h3("#{user.name} follows:")
        # TODO follows - if available   and link to search
        h3("#{user.name} wrote:")
        # TODO posts - always   and link to search
    )
