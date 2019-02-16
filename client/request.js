/* istanbul ignore file */
const http = require('http')

module.exports = function httpRequest(body) {
  return new Promise((resolve, reject) => {
    const request = http.request(
      {
        hostname: 'server',
        port: 8653,
        path: '/graphql',
        method: 'POST',
        headers: {
          'Content-Type': 'application/graphql; charset=UTF-8',
          'X-Requested-With': 'Node.js',
        },
      },
      response => {
        let xbody = ''
        response.setEncoding('utf8')
        response.on('data', d => {
          xbody += d
        })
        response.on('end', () => {
          const { statusCode } = response
          if (statusCode < 400 && statusCode >= 200) {
            resolve(JSON.parse(xbody))
          } else {
            reject(JSON.parse(xbody))
          }
        })
      }
    )
    request.write(body)
    request.end()
  })
}
