cookie = require('./cookie')

# Takes a form HTML element
# And returns an object of the fields in the format:
# {name: value, name: value}
# From HTML to Model `set`/`save`
formData = (form) ->
    data = {}
    fields = form.querySelectorAll('input, textarea, select')
    for field in fields
        data[field.name] = switch field.tagName.toLowerCase()
            when 'input'
                field.value
            when 'textarea'
                field.value
            when 'select'
                field.options[field.selectedIndex].value
    return data

# Determine if the user is logged in
isLoggedIn = ->
    return cookie.get('logged_in') is '1'

# Capitalizes the first letter of a string
ucfirst = (str) ->
    return str.charAt(0).toUpperCase() + str.slice(1)

# Replaces dashes and spaces with underscores, ready to be used in an URL
underscored = (str) ->
    return str.replace(/[-\s]+/g, '_').toLowerCase()

module.exports = {
    formData: formData
    isLoggedIn: isLoggedIn
    ucfirst: ucfirst
    underscored: underscored
}
