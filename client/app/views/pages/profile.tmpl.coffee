{div, h1, p} = require('../../modules/tags')

module.exports = (data) ->
    [id] = data.routeArgs
    user = data.users?[id]
    return div({className: 'spinner'}) unless user

    return div(
        {id: 'terms', className: 'col-10'}
        # TODO avatar
        h1(user.name)
        # TODO created (ago)
        # TODO sets - if available   and link to search
        # TODO follows - if available   and link to search
        # TODO posts - always   and link to search
    )
