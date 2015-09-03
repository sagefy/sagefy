{div, h1, p} = require('../../modules/tags')

module.exports = (data) ->
    [id] = data.routeArgs
    user = data.users?[id]
    return div(
        {id: 'terms', className: 'col-10'}
        if user \
            then content(user) \
            else div({className: 'spinner'})
    )

content = (user) ->
    # TODO avatar
    h1(user.name)
    # TODO created (ago)
    # TODO sets - if available   and link to search
    # TODO follows - if available   and link to search
    # TODO posts - always   and link to search
