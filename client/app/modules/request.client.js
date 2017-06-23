const { parseJSON, isString, convertDataToGet } = require('./utilities')

module.exports = function ajax({ method, url, data }) {
    method = method.toUpperCase()
    if (method === 'GET') {
        url = convertDataToGet(url, data)
    }
    const request = new XMLHttpRequest()
    request.open(method, url, true)
    request.setRequestHeader('X-Requested-With', 'XMLHttpRequest')
    request.setRequestHeader(
        'Content-Type',
        'application/json; charset=UTF-8'
    )
    const promise = new Promise((resolve, reject) => {
        request.onload = function onload() {
            if (this.status < 400 && this.status >= 200) {
                resolve(parseJSON(this.responseText))
            } else {
                reject(parseAjaxErrors(this))
            }
        }
        request.onerror = function onerror() {
            reject(null)
        }
    })
    if (method === 'GET') {
        request.send()
    } else {
        request.send(JSON.stringify(data || {}))
    }
    return promise
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
