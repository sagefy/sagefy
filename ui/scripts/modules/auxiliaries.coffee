cookie = require('./cookie')

aux = {}

# Determine if the user is logged in
aux.isLoggedIn = ->
    return cookie.get('logged_in') is '1'

# Capitalizes the first letter of a string
aux.ucfirst = (str) ->
    return str.charAt(0).toUpperCase() + str.slice(1)

# Replaces dashes and spaces with underscores, ready to be used in an URL
aux.underscored = (str) ->
    return str.replace(/[-\s]+/g, '_').toLowerCase()

# From Handlebars
aux.escape = (str) ->
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
# TODO: move copy to content directory
aux.timeAgo = (str) ->
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


# Return a variable friendly name of the title
aux.slugify = (s) ->
    return s.toLowerCase().replace(/[-\s]+/g, '_')

module.exports = aux
