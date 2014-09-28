_ = require('./utilities')

validations = {}

validations.required = (val) ->
    if val is null or val is undefined or
       (_.isString(val) and val is '')
        return 'Required.'

validations.email = (val) ->
    if not _.isString(val) or not val.match(/^\S+@\S+\.\S+$/)
        return 'Must be an email.'

validations.minlength = (val, len) ->
    if (not _.isString(val) and not _.isArray(val)) or val.length < len
        return "Must be a minimum of #{len}."

module.exports = validations
