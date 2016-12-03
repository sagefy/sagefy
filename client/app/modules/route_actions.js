const store = require('./store')
const tasks = require('./tasks')
const qs = require('./query_string')

const request = () => {
    return window.location.pathname + window.location.search
}

const getQueryParams = (path) => {
    if (path.indexOf('?') === -1) { return {} }
    return qs.get(path.split('?')[1])
}

const route = (path) => {
    store.dispatch({
        type: 'SET_ROUTE',
        route: path,
        routeQuery: getQueryParams(path)
    })
    if (tasks.onRoute) { return tasks.onRoute(path) }
}

if (typeof window !== 'undefined') {
    window.onpopstate = () => {
        route(request())
    }
}

tasks.add({
    route: (path) => {
        if (path !== request()) {
            history.pushState({}, '', path)
            route(path)
        }
    }
})

module.exports = {route}
