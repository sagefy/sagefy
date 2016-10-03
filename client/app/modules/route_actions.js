const store = require('./store')
const tasks = store.tasks
const recorder = require('./recorder')
const qs = require('./query_string')

const request = () => {
    return window.location.pathname + window.location.search
}

const getQueryParams = (path) => {
    if (path.indexOf('?') === -1) { return {} }
    return qs.get(path.split('?')[1])
}

const route = (path) => {
    recorder.emit('route', path)
    store.data.route = path
    store.data.routeQuery = getQueryParams(path)
    if (tasks.onRoute) { tasks.onRoute(path) }
    store.change()
}

window.onpopstate = () => {
    route(request())
}

store.add({
    route: (path) => {
        if (path !== request()) {
            history.pushState({}, '', path)
            route(path)
        }
    }
})

module.exports = {route}
