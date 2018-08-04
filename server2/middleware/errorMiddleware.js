/* eslint-disable max-params */
module.exports = function errorMiddleware(err, req, res, next) {
  if (err.statusCode) {
    res.status(err.statusCode).json({ ...err.json, ref: err.ref })
  } else if (err) {
    res
      .status(500)
      .json({
        errors: [{ message: 'Server error.' }],
        ref: 'UilnKcaD20CQRWAFc4s8Eg',
      })
  }
  next(err)
}
/* eslint-enable */
