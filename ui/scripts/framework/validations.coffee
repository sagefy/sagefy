_ = require('./utilities')
g = require('../modules/content').get

validations = {}

validations.required = (val) ->
    if val is null or val is undefined or
       (_.isString(val) and val is '')
        return g('error', 'required')

validations.email = (val) ->
    if not _.isString(val) or not val.match(/^\S+@\S+\.\S+$/)
        return g('error', 'email')

validations.minlength = (val, len) ->
    if (not _.isString(val) and not _.isArray(val)) or val.length < len
        return g('error', 'minlength').replace('{length}', len)

module.exports = validations
