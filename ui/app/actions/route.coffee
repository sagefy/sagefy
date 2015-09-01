store = require('../modules/store')
actions = store.actions

store.add({
    onRoute: (path) ->
        if path is '/settings'
            store.actions.openSettingsRoute()

    openSettingsRoute: ->
        if not @data.currentUserID or not @data.users?[@data.currentUserID]
            actions.getCurrentUser()
})
