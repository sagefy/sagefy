###
Make an Ajax call given options:
- method: one of get, post, put, delete
- url: string URL
- data: data to send to the server
- done: a function to do on success
    - (json, request) ->
- fail: a function to do on fail
    - (json, request) ->
###
{extend, parseJSON, copy, isString} = require('./utilities')

ajax = ({method, url, data, done, fail, always}) ->
    method = method.toUpperCase()
    if method is 'GET'
        url += if url.indexOf('?') > -1 then '&' else '?'
        url += parameterize(extend(
            data or {}
            {_: (+new Date())}  # Cachebreaker
        ))
    request = new XMLHttpRequest()
    request.open(method, url, true)
    request.setRequestHeader('X-Requested-With', 'XMLHttpRequest')
    request.setRequestHeader(
        'Content-Type'
        'application/json; charset=UTF-8'
    )
    request.onload = ->
        if 400 > @status >= 200
            done(parseJSON(@responseText), this)
        else
            fail(parseAjaxErrors(this), this)
        if always then always()
    request.onerror = ->
        fail(null, this)
        if always then always()
    if method is 'GET'
        request.send()
    else
        request.send(JSON.stringify(data or {}))
    return request

# Convert an object to a query string for GET requests.
parameterize = (obj) ->
    obj = copy(obj)
    pairs = []
    for key, value of obj
        pairs.push(
            encodeURIComponent(key) +
            '=' +
            encodeURIComponent(value)
        )
    return pairs.join('&').replace(/%20/g, '+')

# Try to parse the errors array or just return the error text.
parseAjaxErrors = (r) ->
    return null if not r.responseText
    errors = parseJSON(r.responseText)
    return errors if isString(errors)
    return errors.errors

module.exports = {ajax, parameterize, parseAjaxErrors}
