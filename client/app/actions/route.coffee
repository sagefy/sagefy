store = require('../modules/store')
actions = store.actions
{matchesRoute, ucfirst} = require('../modules/auxiliaries')

routes = [
    {path: '/settings', action: 'openSettingsRoute'}
    {path: '/notices', action: 'listNotices'}
    {path: '/users/{id}', action: 'openProfileRoute'}
    {path: '/my_sets', action: 'listUserSets'}
    {path: '/follows', action: 'listFollows'}
    {path: '/units/{id}', action: 'openUnitRoute'}
    {path: '/sets/{id}', action: 'openSetRoute'}
    {path: '/cards/{id}', action: 'openCardRoute'}
    {path: '/{kind}s/{id}/versions', action: 'openVersionsRoute'}
    {path: '/topics/{id}', action: 'openTopicRoute'}
    {path: '/sets/{id}/tree', action: 'openTreeRoute'}
]


module.exports = store.add({
    onRoute: (path) ->
        for route in routes
            if args = matchesRoute(path, route.path)
                return actions[route.action].apply(null, args)

    openSettingsRoute: ->
        if not @data.currentUserID or not @data.users?[@data.currentUserID]
            actions.getCurrentUser()

    openProfileRoute: (id) ->
        actions.getUser(id, {
            avatar: 12 * 10
            sets: true
            follows: true
            posts: true
        })

    openUnitRoute: (id) ->
        actions.getUnit(id)
        actions.askFollow(id)

    openSetRoute: (id) ->
        actions.getSet(id)
        actions.askFollow(id)

    openCardRoute: (id) ->
        actions.getCard(id)
        actions.askFollow(id)

    openVersionsRoute: (kind, id) ->
        actions["list#{ucfirst(kind)}Versions"](id)

    openTopicRoute: (id) ->
        actions.listPosts(id)
        actions.askFollow(id)

    openTreeRoute: (id) ->
        actions.getSetTree(id)
})
