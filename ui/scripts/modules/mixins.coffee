_ = require('underscore')
$ = require('jquery')
require('jquery.cookie')

# Takes a form html element
# And returns an object of the fields in the format:
# {name: value, name: value}
# From HTML to Backbone.set/save
formData = ($form) ->
    _($form.serializeArray()).reduce((obj, field) ->
        obj[field.name] = field.value
        obj
    , {})

# Try to parse a string as JSON
# Otherwise just return the string
parseJSON = (str) ->
    try
        return JSON.parse(str)
    catch e
        return str

# Determine if the user is logged in
isLoggedIn = ->
    return $.cookie('logged_in') == '1'

# Try to parse the errors array
# Or just return the error text
parseAjaxError = (error) ->
    return parseJSON(error.responseText)?.errors or error.responseText

# Very simple email string validation
validEmail = (val) ->
    return /\S+@\S+\.\S+/.test(val)

# Validates a field one off,
# Expects field to be formatted as in models
# Can validated `required`, `email`, and `minlength`
validateField = (field, val) ->
    test = field.validations

    if test.required and not val
        return {
            name: field.name
            message: "Please enter #{field.name}."
        }

    if test.email and not validEmail(val)
        return {
            name: field.name
            message: "Please enter a valid email address."
        }

    if test.minlength and val.length < test.minlength
        return {
            name: field.name
            message: "Please enter at least #{test.minlength} " +
                "characters in #{field.name}."
        }

    return false  # `false` meaning there's no error

# Iterates over model's attributes and validates all of them
# Used when submitting a model
# Perfect for Backbone.Model.validate
# Returns an array of errors or `undefined`
validateModelFromFields = (attrs = {}) ->
    errors = []

    for field in @fields  # where @ is model
        val = attrs[field.name]

        error = validateField(field, val)
        if error
            errors.push(error)

    if errors.length
        return errors

# Capitalizes the first letter of a string
ucfirst = (str) ->
    return str.charAt(0).toUpperCase() + str.slice(1)

# Replaces dashes and spaces with underscores, ready to be used in an URL
underscored = (str) ->
    return str.replace(/[-\s]+/g, '_').toLowerCase()

module.exports = {
    formData: formData
    isLoggedIn: isLoggedIn
    parseJSON: parseJSON
    parseAjaxError: parseAjaxError
    validEmail: validEmail
    validateField: validateField
    validateModelFromFields: validateModelFromFields
    ucfirst: ucfirst
    underscored: underscored
}
