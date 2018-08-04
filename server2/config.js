// Nota bene: For production empty this file.
//            Then copy and paste config.prod.js into this file instead.
//            Then update mail.sender, mail.password, & session.secret

/* eslint-disable global-require */

if (process.env.TRAVIS) {
  module.exports = require('./config.travis')
} else if (process.env.NODE_ENV === 'test') {
  module.exports = require('./config.test')
} else {
  module.exports = require('./config.dev')
}
