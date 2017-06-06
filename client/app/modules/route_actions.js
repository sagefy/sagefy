const { dispatch } = require('./store')
const tasks = require('./tasks')
const qs = require('./query_string')
const pageTitles = require('../modules/page_titles')
const { matchesRoute } = require('../modules/auxiliaries')

const request = () => {
    return window.location.pathname + window.location.search
}

const getQueryParams = (path) => {
    if (path.indexOf('?') === -1) { return {} }
    return qs.get(path.split('?')[1])
}

const findTitle = (path) => {
    for (let i = 0; i < pageTitles.length; i++) {
        const route = pageTitles[i]
        const args = matchesRoute(path, route.path)
        if (args) {
            return route.title
        }
    }
}

const route = (path) => {
    dispatch({
        type: 'SET_ROUTE',
        route: path,
        routeQuery: getQueryParams(path),
        title: findTitle(path),
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

module.exports = { route }
