###
Auxiliaries are utlity functions that are specific to Sagefy.
###

cookie = require('./cookie')
{copy, isString} = require('./utilities')

# Determine if the user is logged in
isLoggedIn = ->
    return cookie.get('logged_in') is '1'

# Capitalizes the first letter of a string
ucfirst = (str) ->
    return str.charAt(0).toUpperCase() + str.slice(1)

# Replaces dashes and spaces with underscores, ready to be used in an URL
underscored = (str) ->
    return str.replace(/[-\s]+/g, '_').toLowerCase()

# From Handlebars
escape = (str) ->
    chars = {
        '&': '&amp;'
        '<': '&lt;'
        '>': '&gt;'
        '"': '&quot;'
        '\'': '&#x27;'
        '`': '&#x60;'
    }

    return ('' + str).replace(/[&<>"'`]/g, (char) ->
        return chars[char]
    )

# From http://ejohn.org/files/pretty.js
# TODO move copy to content directory
timeAgo = (str) ->
    diff = (new Date()).getTime() - (new Date(str)).getTime()
    days = Math.floor(diff / 86400000)
    hours = Math.floor(diff / 3600000)
    minutes = Math.floor(diff / 60000)
    return "#{days} days ago" if days > 1
    return 'Yesterday' if days is 1
    return "#{hours} hours ago" if hours > 1
    return '1 hour ago' if hours is 1
    return "#{minutes} minutes ago" if minutes > 1
    return '1 minute ago' if minutes is 1
    return 'Just now'

# Return a variable friendly name of the title.
slugify = (s) ->
    return s.toLowerCase().replace(/[-\s]+/g, '_')

# Set the page title.
setTitle = (title = 'FIX ME') ->
    title = "#{title} – Sagefy"
    if document.title isnt title
        document.title = title

# Wait for function to stop being called for `delay`
# milliseconds, and then finally call the real function.
debounce = (fn, delay) ->
    timer = null
    return (args...) ->
        clearTimeout(timer)
        timer = setTimeout(=>
            fn.apply(this, args)
        , delay)

# Determine if a given path matches this router.
# Returns either false or array, where array is matches parameters.
matchesRoute = (docPath, viewPath) ->
    if isString(viewPath)
        viewPath = new RegExp(
            '^' +
            viewPath.replace(/\{([\d\w\_\$]+)\}/g, '([^/]+)') +
            '$'
        )
    match = docPath.match(viewPath)
    return if match then match.slice(1) else false

# Returns an object of the fields' value
getFormValues = (form) ->
    data = {}
    for field in form.querySelectorAll('input, textarea')
        data[field.name] = field.value
    return data

mergeFieldsData = (fields, data) ->
    fields_ = copy(fields)

    for error in data.errors or []
        field = fields_.filter((f) -> f.name is error.name)?[0]
        field.error = error.message if field

    for name, value of data.formData or {}
        field = fields_.filter((f) -> f.name is name)?[0]
        field.value = value if field

    if data.sending
        field = fields_.filter((f) -> f.type is 'submit')?[0]
        field.disabled = true if field

    return fields_

module.exports = {
    isLoggedIn
    ucfirst
    underscored
    escape
    timeAgo
    slugify
    setTitle
    debounce
    matchesRoute
    getFormValues
    mergeFieldsData
}
