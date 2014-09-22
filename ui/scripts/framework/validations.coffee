validations = {}

validations.required = (val) ->
    return 'Required.' if val is null or val is undefined

validations.email = (val) ->
    return 'Must be an email.' if not val.match(/^\S+@\S+\.\S+$/)

validations.minlength = (val, len) ->
    return "Must be a minimum of #{len}." if val.length < len

module.exports = validations
