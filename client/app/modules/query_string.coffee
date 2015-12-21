{valuefy} = require('./auxiliaries')

get = (query) ->
    query or= window.location.search.substring(1)
    return {} if not query
    params = query.split('&')
    data = {}
    for param in params
        [key, value] = param.split('=')
        data[decodeURIComponent(key)] = valuefy(value)
    return data

module.exports = {valuefy, get}
