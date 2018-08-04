/* eslint-disable max-params */
module.exports = function errorMiddleware(err, req, res, next) {
  // TODO update this to handle errors thrown in middleware
  if (err.message === 'access denied') {
    res.status(403)
    res.json({ error: err.message })
  }
  next(err)
}
/* eslint-enable */
