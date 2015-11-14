store = require('./store')
actions = store.actions
recorder = require('./recorder')

request = ->
    return window.location.pathname + window.location.search

route = (path) ->
    recorder.emit('route', path)
    store.data.route = path
    actions.onRoute(path) if actions.onRoute
    store.change()

window.onpopstate = ->
    route(request())

store.add({
    route: (path) ->
        if path isnt request()
            history.pushState({}, '', path)
            route(path)
})

module.exports = {route}
