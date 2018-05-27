// Determine if a given path matches this router.
// Returns either false or array, where array is matches parameters.
const isString = require('lodash.isstring')

module.exports = function matchesRoute(docPath, viewPath) {
  if (!docPath) {
    return false
  }
  ;[docPath] = docPath.split('?') // Only match the pre-query params
  if (isString(viewPath)) {
    viewPath = new RegExp(
      `^${viewPath.replace(/\{([\d\w\-_$]+)\}/g, '([^/]+)')}$`
    )
  }
  const match = docPath.match(viewPath)
  return match ? match.slice(1) : false
}
