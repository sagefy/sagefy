store = require('./store')
recorder = require('./recorder')

store.data.route = window.location.pathname

module.exports = store.add({
    route: (path) ->
        if path isnt window.location.pathname
            recorder.emit('route', path)
            history.pushState({}, '', path)
            store.data.route = path
            store.change()
})
