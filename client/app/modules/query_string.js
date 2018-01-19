const { valuefy } = require('./auxiliaries')

const get = query => {
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

module.exports = { valuefy, get }
