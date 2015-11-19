store = require('../modules/store')
actions = store.actions
{matchesRoute, ucfirst} = require('../modules/auxiliaries')

store.add({
    onRoute: (path) ->
        # TODO remove duplicated effort with index.tmpl
        if path is '/settings'
            actions.openSettingsRoute()
        if path is '/notices'
            actions.openNoticesRoute()
        if args = matchesRoute(path, '/users/{id}')
            actions.openProfileRoute(args[0])
        if path is '/my_sets'
            actions.listUserSets()
        if path is '/follows'
            actions.listFollows()
        if args = matchesRoute(path, '/units/{id}')
            actions.getUnit(args[0])
            actions.askFollow(args[0])
        if args = matchesRoute(path, '/sets/{id}')
            actions.getSet(args[0])
            actions.askFollow(args[0])
        if args = matchesRoute(path, '/cards/{id}')
            actions.getCard(args[0])
            actions.askFollow(args[0])
        if args = matchesRoute(path, '/{kind}s/{id}/versions')
            actions["list#{ucfirst(args[0])}Versions"](args[1])

    openSettingsRoute: ->
        if not @data.currentUserID or not @data.users?[@data.currentUserID]
            actions.getCurrentUser()

    openNoticesRoute: ->
        actions.listNotices()

    openProfileRoute: (id) ->
        actions.getUser(id, {
            avatar: 12 * 10
            sets: true
            follows: true
            posts: true
        })
})
