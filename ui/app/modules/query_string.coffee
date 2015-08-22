valuefy = (value) ->
    return true if value is 'true'
    return false if value is 'false'
    return null if value is 'null'
    return parseFloat(value) if value.match(/^\d+\.\d+$/)
    return parseInt(value) if value.match(/^\d+$/)
    return decodeURIComponent(value)

get = (query) ->
    query or= window.location.search.substring(1)
    params = query.split('&')
    data = {}
    for param in params
        [key, value] = param.split('=')
        data[decodeURIComponent(key)] = valuefy(value)
    return data

module.exports = {valuefy, get}
