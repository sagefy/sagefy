const abort = require('../helpers/abort')

module.exports = function authMiddleware(req, res, next) {
  if (!req.session.user) {
    throw abort(401, 'GlqI6VAROUCGqZy3OuKJ1A')
  }
  next()
}
