const http = require('http')
const { convertDataToGet, isString } = require('./utilities')

module.exports = function httpRequest({ method, url, data }) {
    method = method.toUpperCase()
    if (method === 'GET') {
        url = convertDataToGet(url, data)
    }
    let done
    let fail
    const promise = new Promise((resolve, reject) => {
        done = resolve
        fail = reject
    })
    const request = http.request(
        {
            hostname: 'server',
            port: 8653,
            path: url,
            method: method,
            headers: {
                'Content-Type': 'application/json; charset=UTF-8',
                'X-Requested-With': 'Node.js',
                Cookie: global.requestCookie || '',
            },
        },
        (response) => {
            let body = ''
            response.setEncoding('utf8')
            response.on('data', (d) => {
                body += d
            })
            response.on('end', () => {
                let responseData = ''
                try {
                    responseData = JSON.parse(body)
                } catch (e) {
                    responseData = body
                }
                const statusCode = response.statusCode
                if (statusCode < 400 && statusCode >= 200) {
                    done(responseData)
                } else if (isString(responseData)) {
                    fail(responseData)
                } else {
                    fail(responseData.errors)
                }
            })
        }
    )
    if (method !== 'GET') {
        request.write(JSON.stringify(data || {}))
    }
    request.end()
    return promise
}
