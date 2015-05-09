get = (query) ->
    query or= window.location.search.substring(1)
    params = query.split('&')
    data = {}
    for param in params
        [key, value] = param.split('=')
        data[decodeURIComponent(key)] = switch
            when value is 'true'
                true
            when value is 'false'
                false
            when value.match(/^\d+\.\d+$/)
                parseFloat(value)
            when value.match(/^\d+$/)
                parseInt(value)
            else
                decodeURIComponent(value)
    return data

module.exports = {get: get}
