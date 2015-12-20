store = require('./store')
tasks = store.tasks
recorder = require('./recorder')
qs = require('./query_string')

request = ->
    return window.location.pathname + window.location.search

getQueryParams = (path) ->
    return {} if path.indexOf('?') is -1
    return qs.get(path.split('?')[1])

route = (path) ->
    recorder.emit('route', path)
    store.data.route = path
    store.data.routeQuery = getQueryParams(path)
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
