const http = require('http')
const {extend, parameterize, isString} = require('./utilities')

module.exports = function httpRequest({method, url, data, done, fail, always}) {
    method = method.toUpperCase()
    if (method === 'GET') {
        url += url.indexOf('?') > -1 ? '&' : '?'
        url += parameterize(extend(
            data || {},
            {_: +new Date()}  // Cachebreaker
        ))
    }
    const request = http.request({
        hostname: 'localhost',
        port: 8653,
        path: url,
        method: method,
        headers: {
            'Content-Type': 'application/json; charset=UTF-8',
            'X-Requested-With': 'Node.js',
        }
    }, (response) => {
        let body = ''
        response.setEncoding('utf8')
        response.on('data', (d) => { body += d })
        response.on('end', () => {
            const responseData = JSON.parse(body)
            const statusCode = response.statusCode
            if(statusCode < 400 && statusCode >= 200) {
                done(responseData)
            } else if (isString(responseData)) {
                fail(responseData)
            } else {
                fail(responseData.errors)
            }
            if (always) {
                always()
            }
        })
    })
    if(method !== 'GET') {
        request.write(JSON.stringify(data || {}))
    }
    request.end()
    return request
}
