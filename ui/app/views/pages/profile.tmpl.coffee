{div, h1, p} = require('../../modules/tags')

module.exports = (data) ->
    [id] = data.routeArgs
    user = data.users?[id]
    return div(
        {id: 'terms', className: 'col-10'}
        h1('Profile')
        if user \
            then content(user) \
            else div({className: 'spinner'})
    )

content = (user) ->
    div(user.name)
