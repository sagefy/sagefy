/* istanbul ignore file */
const http = require('http')

function parseJSON(data) {
  try {
    return JSON.parse(data)
  } catch (e) {
    return data
  }
}

module.exports = function gqlRequest({ query, variables, jwtToken }) {
  return new Promise((resolve, reject) => {
    const request = http.request(
      {
        hostname: '127.0.0.1',
        port: 8653,
        path: '/graphql',
        method: 'POST',
        headers: {
          'Content-Type': 'application/json; charset=UTF-8',
          Accept: 'application/json',
          'X-Requested-With': 'Node.js',
          Authorization: jwtToken ? `Bearer ${jwtToken}` : null,
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
            resolve(parseJSON(xbody))
          } else {
            reject(parseJSON(xbody))
          }
        })
      }
    )
    request.write(JSON.stringify({ query, variables }))
    request.end()
  })
}
