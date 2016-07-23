###
Auxiliaries are utlity functions that are specific to Sagefy.
###

cookie = require('./cookie')
{extend, copy, isString, isArray} = require('./utilities')

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
# TODO-3 move copy to content directory
timeAgo = (str) ->
    diff = (new Date()).getTime() - (new Date(str)).getTime()
    days = Math.floor(diff / (24 * 60 * 60 * 1000))
    hours = Math.floor(diff / (60 * 60 * 1000))
    minutes = Math.floor(diff / (60 * 1000))
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
    docPath = docPath.split('?')[0]  # Only match the pre-query params
    if isString(viewPath)
        viewPath = new RegExp(
            '^' +
            viewPath.replace(/\{([\d\w\_\$]+)\}/g, '([^/]+)') +
            '$'
        )
    match = docPath.match(viewPath)
    return if match then match.slice(1) else false

valuefy = (value) ->
    return true if value is 'true'
    return false if value is 'false'
    return null if value is 'null'
    return parseFloat(value) if value.match(/^\d+\.\d+$/)
    return parseInt(value) if value.match(/^\d+$/)
    return decodeURIComponent(value)

truncate = (str, len) ->
    return str if str.length <= len
    return str.slice(0, len) + '...'

compact = (A) ->
    return (a for a in A when a)

mergeArraysByKey = (A, B, key = 'id') ->
    a = 0
    b = 0
    C = []

    A = compact(A)
    B = compact(B)

    console.log(A, B)
    console.log(A.length, B.length)

    while a < A.length
        b2 = b
        found = false

        while b2 < B.length
            if A[a][key] is B[b2][key]
                while b <= b2
                    C.push(B[b])
                    b++
                found = true
                break
            b2++

        if not found
            C.push(A[a])

        a++

    while b < B.length
        C.push(B[b])
        b++

    return C

# Returns an object of the fields' value
getFormValues = (form) ->
    data = {}
    for el in form.querySelectorAll([
        'input[type="text"]'
        'input[type="email"]'
        'input[type="password"]'
        'input[type="hidden"]'
        'textarea'
    ].join(', '))
        data[el.name] = valuefy(el.value)

    for el in form.querySelectorAll('[type=radio]')
        data[el.name] = valuefy(el.value) if el.checked

    for el in form.querySelectorAll('[type=checkbox]')
        data[el.name] ?= []
        data[el.name].push(valuefy(el.value)) if el.checked

    return data

# Given a forms values as an object, parse any fields with `.`
# in them to create a save-able object for the service
parseFormValues = (data) ->
    output = {}

    for key, value of data
        if key.indexOf('.') is -1
            output[key] = value
        else
            prev = output
            names = key.split('.').map((n) ->
                if (/^\d+$/).test(n) then parseInt(n) else n)
            for name, i in names
                if i is names.length - 1
                    prev[name] = value
                else
                    next = names[i + 1]
                    if typeof next is 'string'
                        prev[name] ?= {}
                    else if typeof next is 'number'
                        prev[name] ?= []
                    prev = prev[name]

    return output

# Validate the entry with the given ID against the schema.
# Returns a list of errors.
# Use this method for any sort of `create` or `update` call.
validateFormData = (data, schema, fields) ->
    errors = []
    for fieldName in (fields or Object.keys(schema))
        for fn in schema[fieldName].validations
            error = if isArray(fn)
                fn[0](data[fieldName], fn.slice(1)...)
            else
                fn(data[fieldName])
            if error
                errors.push({
                    name: fieldName
                    message: error
                })
                break
    return errors

# Given a schema, fields, errors, formData, and sending boolean (optional)
# create a list of fields with all the data needed to create the form
# correctly.
createFieldsData = ({
    schema
    fields
    errors = []
    formData = {}
    sending = false
}) ->
    fields = copy(fields)

    for field, i in fields
        fields[i] = extend({}, schema[field.name], field)

    for error in errors
        field = fields.filter((f) -> f.name is error.name)?[0]
        field.error = error.message if field

    for name, value of formData
        # All of this for the list input type
        if matches = name.match(/^(.*)\.(\d+)\.(.*)$/)
            [full, pre, index, col] = matches
            field = fields.filter((f) -> f.name is pre)?[0]
            if field
                field.value ?= []
                field.value[index] ?= {}
                field.value[index][col] = value
        # For every other kind of field...
        else
            field = fields.filter((f) -> f.name is name)?[0]
            field.value = value if field

    if sending
        field = fields.filter((f) -> f.type is 'submit')?[0]
        field.disabled = true if field

    return fields

prefixObjectKeys = (prefix, obj) ->
    next = {}
    for name, value of obj
        next[prefix + name] = value
    return next

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
    truncate
    mergeArraysByKey
    valuefy

    getFormValues
    parseFormValues
    validateFormData
    createFieldsData

    prefixObjectKeys
    compact
}
