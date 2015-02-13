Events = require('./events')
util = require('./utilities')

###
The adapter is responsible for
- handling a route,
- creating instances of models and views,
- handling model and view events, and
- cleaning up after the route is finished.
###

class Adapter extends Events
    # **constructor**
    # When a route is hit, the constructor will be called.
    # Here, models and views should be defined, and listeners to the
    # views and models should bind here.
    # Additional methods can be defined to handle model and view events.

    # **remove**
    # When a different route is hit, the current adapter is removed.
    # Here, clean up the models, views, and event bindings.

    # The app fetches the URLs from the adapters and registers them
    # with the router
    # URL allows for plain string, RegExp, and also the format
    # /foo/{id}/bar/{slug}
    url: ''

    # Determine if a given path matches this router
    # Returns either false or array, where array is matches parameters
    matches: (path) ->
        @urlRegExp or= @getUrlRegExp(@url)
        match = path.match(@urlRegExp)
        return if match then match.slice(1) else false

    # Converts a string representation of URL to a RegExp representation
    getUrlRegExp: (url) ->
        return url if util.isRegExp(url)
        url = url() if util.isFunction(url)
        return new RegExp(
            '^' +
            url.replace(/\{([\d\w\_\$]+)\}/g, '([^/]+)') +
            '$'
        )

module.exports = Adapter
