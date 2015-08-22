store = require('./store')
recorder = require('./recorder')

store.data.route = window.location.pathname

route = (path) ->
    recorder.emit('route', path)
    store.data.route = path
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
