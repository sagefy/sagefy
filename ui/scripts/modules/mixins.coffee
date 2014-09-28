cookie = require('./cookie')

mixins = {}

# Determine if the user is logged in
mixins.isLoggedIn = ->
    return cookie.get('logged_in') is '1'

# Capitalizes the first letter of a string
mixins.ucfirst = (str) ->
    return str.charAt(0).toUpperCase() + str.slice(1)

# Replaces dashes and spaces with underscores, ready to be used in an URL
mixins.underscored = (str) ->
    return str.replace(/[-\s]+/g, '_').toLowerCase()

module.exports = mixins
