###
Validations are functions which return string if there's an issue
or a nothing if okay.
###

util = require('../modules/utilities')
c = require('../modules/content').get

isBlank = (val) ->
    return val is null or val is undefined or
       (util.isString(val) and val is '')

# Validation functions should return a string on error,
# or return nothing if there is no problem.

# Require there to be content.
required = (val) ->
    return c('required') if isBlank(val)


# Require the field to be an email address if value is present.
email = (val) ->
    return c('email') if (not isBlank(val) and (
        not util.isString(val) or
        not val.match(/^\S+@\S+\.\S+$/)
    ))

# Require the field to contain a minimum length if value is present.
minlength = (val, len) ->
    return c('minlength').replace('{length}', len) if(not isBlank(val) and (
        (util.isString(val) or util.isArray(val)) and
        val.length < len
    ))

module.exports = {required, email, minlength}
