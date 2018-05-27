const { writeGetUrl, parseJSON, parseAjaxErrors } = require('./url')

module.exports = function ajax({ method, url, data }) {
  method = method.toUpperCase()
  if (method === 'GET') {
    url = writeGetUrl(url, data)
  }
  const request = new XMLHttpRequest()
  request.open(method, url, true)
  request.setRequestHeader('X-Requested-With', 'XMLHttpRequest')
  request.setRequestHeader('Content-Type', 'application/json; charset=UTF-8')
  const promise = new Promise((resolve, reject) => {
    request.onload = function onload() {
      if (this.status < 400 && this.status >= 200) {
        resolve(parseJSON(this.responseText))
      } else {
        reject(parseAjaxErrors(this.responseText))
      }
    }
    request.onerror = function onerror() {
      reject(Error())
    }
  })
  if (method === 'GET') {
    request.send()
  } else {
    request.send(JSON.stringify(data || {}))
  }
  return promise
}
