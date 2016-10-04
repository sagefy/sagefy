/*
Make an Ajax call given options:
- method: one of get, post, put, delete
- url: string URL
- data: data to send to the server
- done: a function to do on success
    - (json, request) =>
- fail: a function to do on fail
    - (json, request) =>
*/
const {extend, parseJSON, copy, isString} = require('./utilities')

const ajax = function ({method, url, data, done, fail, always}) {
    method = method.toUpperCase()
    if (method === 'GET') {
        url += url.indexOf('?') > -1 ? '&' : '?'
        url += parameterize(extend(
            data || {},
            {_: (+new Date())}  // Cachebreaker
        ))
    }
    const request = new XMLHttpRequest()
    request.open(method, url, true)
    request.setRequestHeader('X-Requested-With', 'XMLHttpRequest')
    request.setRequestHeader(
        'Content-Type',
        'application/json; charset=UTF-8'
    )
    request.onload = function () {
        if (400 > this.status && this.status >= 200) {
            done(parseJSON(this.responseText), this)
        } else {
            fail(parseAjaxErrors(this), this)
        }
        if (always) { always() }
    }
    request.onerror = function () {
        fail(null, this)
        if (always) { always() }
    }
    if (method === 'GET') {
        request.send()
    } else {
        request.send(JSON.stringify(data || {}))
    }
    return request
}

// Convert an object to a query string for GET requests.
const parameterize = (obj) => {
    obj = copy(obj)
    const pairs = []
    for (const key in obj) {
        const value = obj[key]
        pairs.push(
            encodeURIComponent(key) +
            '=' +
            encodeURIComponent(value)
        )
    }
    return pairs.join('&').replace(/%20/g, '+')
}

// Try to parse the errors array or just return the error text.
const parseAjaxErrors = (r) => {
    if (!r.responseText) { return null }
    const errors = parseJSON(r.responseText)
    if (isString(errors)) { return errors }
    return errors.errors
}

module.exports = {ajax, parameterize, parseAjaxErrors}
