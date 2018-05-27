/*
Auxiliaries are utlity functions that are specific to Sagefy.
*/

const isString = require('lodash.isstring')
const snakeCase = require('lodash.snakecase')
const compact = require('lodash.compact')

// Turns underscore or camel into title case
function titleize(str = '') {
  return snakeCase(str)
    .split('_')
    .map(w => w.charAt(0).toUpperCase() + w.substr(1))
    .join(' ')
}

// Set the page title.
function setTitle(title = 'FIX ME') {
  title = `${title} – Sagefy`
  if (typeof document !== 'undefined' && document.title !== title) {
    document.title = title
  }
}

// Determine if a given path matches this router.
// Returns either false or array, where array is matches parameters.
function matchesRoute(docPath, viewPath) {
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

/* eslint-disable max-statements */
function mergeArraysByKey(A, B, key = 'id') {
  let a = 0
  let b = 0
  const C = []

  A = compact(A)
  B = compact(B)

  while (a < A.length) {
    let b2 = b
    let found = false

    while (b2 < B.length) {
      if (A[a][key] === B[b2][key]) {
        while (b <= b2) {
          C.push(B[b])
          b += 1
        }
        found = true
        break
      }
      b2 += 1
    }

    if (!found) {
      C.push(A[a])
    }

    a += 1
  }

  while (b < B.length) {
    C.push(B[b])
    b += 1
  }

  return C
}
/* eslint-enable max-statements */

function goLogin() {
  if (typeof window !== 'undefined') {
    window.location = '/log_in'
  }
}

module.exports = {
  titleize,
  setTitle,
  matchesRoute,
  mergeArraysByKey,
  goLogin,
}
