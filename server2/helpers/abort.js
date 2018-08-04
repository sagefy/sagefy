const { getStatusText } = require('http-status-codes')

module.exports = function abort(statusCode, ref, json) {
  const abortError = new Error(ref)
  abortError.statusCode = statusCode
  abortError.ref = ref
  abortError.json = json || {
    errors: [{ message: getStatusText(statusCode) }],
  }
  return abortError
}
