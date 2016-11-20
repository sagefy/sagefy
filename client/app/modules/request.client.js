const {extend, parseJSON, isString, parameterize} = require('./utilities')

module.exports = function ajax({method, url, data, done, fail, always}) {
    method = method.toUpperCase()
    if (method === 'GET') {
        url += url.indexOf('?') > -1 ? '&' : '?'
        url += parameterize(extend(
            data || {},
            {_: +new Date()}  // Cachebreaker
        ))
    }
    const request = new XMLHttpRequest()
    request.open(method, url, true)
    request.setRequestHeader('X-Requested-With', 'XMLHttpRequest')
    request.setRequestHeader(
        'Content-Type',
        'application/json; charset=UTF-8'
    )
    request.onload = function onload() {
        if (this.status < 400 && this.status >= 200) {
            done(parseJSON(this.responseText), this)
        } else {
            fail(parseAjaxErrors(this), this)
        }
        if (always) {
            always()
        }
    }
    request.onerror = function onerror() {
        fail(null, this)
        if (always) {
            always()
        }
    }
    if (method === 'GET') {
        request.send()
    } else {
        request.send(JSON.stringify(data || {}))
    }
    return request
}

// Try to parse the errors array or just return the error text.
function parseAjaxErrors(r) {
    if (!r.responseText) {
        return null
    }
    const errors = parseJSON(r.responseText)
    if (isString(errors)) {
        return errors
    }
    return errors.errors
}
