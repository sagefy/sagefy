util = require('./utilities')
g = require('../modules/content').get

# Validation functions should return a string on error,
# or return nothing if there is no problem.
validations = {}

# Require there to be content
validations.required = (val) ->
    if val is null or val is undefined or
       (util.isString(val) and val is '')
        return g('error', 'required')

# Require the field to be an email address if value is present.
validations.email = (val) ->
    if not util.isString(val) or not val.match(/^\S+@\S+\.\S+$/)
        return g('error', 'email')

# Require the field to contain a minimum length if value is present.
validations.minlength = (val, len) ->
    if (not util.isString(val) and not util.isArray(val)) or val.length < len
        return g('error', 'minlength').replace('{length}', len)

module.exports = validations
