store = require('./store')
tasks = store.tasks
recorder = require('./recorder')

request = ->
    return window.location.pathname + window.location.search

route = (path) ->
    recorder.emit('route', path)
    store.data.route = path
    tasks.onRoute(path) if tasks.onRoute
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
