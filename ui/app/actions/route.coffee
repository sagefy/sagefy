store = require('../modules/store')
actions = store.actions

store.add({
    onRoute: (path) ->
        if path is '/settings'
            actions.openSettingsRoute()
        if path is '/notices'
            actions.openNoticesRoute()

    openSettingsRoute: ->
        if not @data.currentUserID or not @data.users?[@data.currentUserID]
            actions.getCurrentUser()

    openNoticesRoute: ->
        actions.listNotices()
})
