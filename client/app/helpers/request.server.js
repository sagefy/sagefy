const http = require('http')
const { writeGetUrl, parseJSON, parseAjaxErrors } = require('./url')

module.exports = function httpRequest({ method, url, data, rq }) {
  method = method.toUpperCase()
  if (method === 'GET') {
    url = writeGetUrl(url, data)
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
      method,
      headers: {
        'Content-Type': 'application/json; charset=UTF-8',
        'X-Requested-With': 'Node.js',
        Cookie: rq || '',
      },
    },
    response => {
      let body = ''
      response.setEncoding('utf8')
      response.on('data', d => {
        body += d
      })
      response.on('end', () => {
        const { statusCode } = response
        if (statusCode < 400 && statusCode >= 200) {
          done(parseJSON(body))
        } else {
          fail(parseAjaxErrors(body))
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
