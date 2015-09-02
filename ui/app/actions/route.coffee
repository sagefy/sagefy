store = require('../modules/store')
actions = store.actions
{matchesRoute} = require('../modules/auxiliaries')

store.add({
    onRoute: (path) ->
        if path is '/settings'
            actions.openSettingsRoute()
        if path is '/notices'
            actions.openNoticesRoute()
        if args = matchesRoute(path, '/users/{id}')
            actions.openProfileRoute(args[0])
        if path is '/my_sets'
            actions.listUserSets()

    openSettingsRoute: ->
        if not @data.currentUserID or not @data.users?[@data.currentUserID]
            actions.getCurrentUser()

    openNoticesRoute: ->
        actions.listNotices()

    openProfileRoute: (id) ->
        actions.getUser(id)
})
