const session = require('express-session')
const RedisStore = require('connect-redis')(session)

const config = require('../config')

const TWO_WEEKS_IN_MS = 1000 * 60 * 60 * 24 * 7 * 2

module.exports = session({
  secret: config.session.secret,
  store: new RedisStore(config.redis),
  cookie: {
    maxAge: TWO_WEEKS_IN_MS,
  },
  resave: false,
  saveUninitialized: false,
})
