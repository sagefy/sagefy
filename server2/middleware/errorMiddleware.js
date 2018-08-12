/* eslint-disable max-params */
const sendMail = require('../helpers/mail')
const config = require('../config')

module.exports = function errorMiddleware(err, req, res, next) {
  if (config.debug) console.error(err) // eslint-disable-line
  if (err.statusCode) {
    res.status(err.statusCode).json({ ...err.json, ref: err.ref })
  } else if (err) {
    sendMail({
      to: 'support@sagefy.org',
      subject: '500 Response',
      body: [req.originalUrl, err.code, err.message, err.stack].join('\n\n'),
    })
    res.status(500).json({
      errors: [{ message: 'Server error.' }],
      ref: 'UilnKcaD20CQRWAFc4s8Eg',
    })
  }
  // TODO Joi validation errors
  next(err)
}
