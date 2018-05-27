const merge = require('lodash.merge')
const cloneDeep = require('lodash.clonedeep')
const valuefy = require('./valuefy')

function read(query) {
  query =
    query ||
    (typeof window !== 'undefined' && window.location.search.substring(1))
  if (!query) {
    return {}
  }
  const params = query.split('&')
  const data = {}
  params.forEach(param => {
    const [key, value] = param.split('=')
    data[decodeURIComponent(key)] = valuefy(value)
  })
  return data
}

// Convert an object to a query string for GET requests.
function parameterize(obj) {
  obj = cloneDeep(obj)
  const pairs = []
  Object.keys(obj).forEach(key => {
    const value = obj[key]
    pairs.push(`${encodeURIComponent(key)}=${encodeURIComponent(value)}`)
  })
  return pairs.join('&').replace(/%20/g, '+')
}

function write(url, data) {
  url += url.indexOf('?') > -1 ? '&' : '?'
  url += parameterize(
    merge(
      data || {},
      { _: +new Date() } // Cachebreaker
    )
  )
  return url
}

module.exports = { read, write }
