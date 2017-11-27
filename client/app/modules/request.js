/* eslint-disable global-require */
if (typeof XMLHttpRequest !== 'undefined') {
  // For browsers use XHR adapter
  module.exports = require('./request.client')
} else if (typeof process !== 'undefined') {
  // For node use HTTP adapter
  module.exports = require('./request.server')
}
