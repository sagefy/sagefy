const { dispatch } = require('./store')
const tasks = require('./tasks')
const { readQueryString } = require('./url')
const pageTitles = require('../helpers/page_titles')
const matchesRoute = require('../helpers/matches_route')

function request() {
  return window.location.pathname + window.location.search
}

function getQueryParams(path) {
  if (path.indexOf('?') === -1) {
    return {}
  }
  return readQueryString(path.split('?')[1])
}

function findTitle(path) {
  for (let i = 0; i < pageTitles.length; i += 1) {
    const xroute = pageTitles[i]
    const args = matchesRoute(path, xroute.path)
    if (args) {
      return xroute.title
    }
  }
  return ''
}

function route(path) {
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
