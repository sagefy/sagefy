store = require('./store')
actions = store.actions
recorder = require('./recorder')

route = (path) ->
    recorder.emit('route', path)
    store.data.route = path
    actions.onRoute(path) if actions.onRoute
    store.change()

window.onpopstate = ->
    route(window.location.pathname)

store.add({
    route: (path) ->
        if path isnt window.location.pathname
            history.pushState({}, '', path)
            route(path)
})

module.exports = {route}
