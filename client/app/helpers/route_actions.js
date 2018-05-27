const { dispatch } = require('./store')
const tasks = require('./tasks')
const qs = require('./query_string')
const pageTitles = require('../helpers/page_titles')
const { matchesRoute } = require('../helpers/auxiliaries')

const request = () => window.location.pathname + window.location.search

const getQueryParams = path => {
  if (path.indexOf('?') === -1) {
    return {}
  }
  return qs.get(path.split('?')[1])
}

const findTitle = path => {
  for (let i = 0; i < pageTitles.length; i += 1) {
    const route = pageTitles[i]
    const args = matchesRoute(path, route.path)
    if (args) {
      return route.title
    }
  }
  return ''
}

const route = path => {
  dispatch({
    type: 'SET_ROUTE',
    route: path,
    routeQuery: getQueryParams(path),
    title: findTitle(path),
  })
  if (tasks.onRoute) {
    return tasks.onRoute(path)
  }
  return null
}

if (typeof window !== 'undefined') {
  window.onpopstate = () => {
    route(request())
  }
}

tasks.add({
  route: path => {
    if (path !== request()) {
      window.history.pushState({}, '', path)
      route(path)
    }
  },
})

module.exports = { route }
