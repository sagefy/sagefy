# TODO add comments

decode = (s) -> decodeURIComponent(s)

module.exports = ->
    query = window.location.search.substring(1)
    params = query.split('&')
    data = {}
    for param in params
        [key, value] = param.split('=')
        data[decode(key)] = decode(value)
    return data
