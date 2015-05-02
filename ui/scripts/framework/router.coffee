###
The router takes a series of views, and delegates URLs
to them when the URL changes.
###

Listener = require('./listener')
util = require('./utilities')
history = window.history

class Router extends Listener
    # URL allows for plain string, RegExp, and also the format:
    # `/foo/{id}/bar/{slug}`
    # Pattern is `['/path', View]`.
    routes: []

    constructor: (@options = {}) ->
        super
        @routes = @options.routes or @routes
        @region = @options.region
        @on('route', @route.bind(this))

    # When the user uses their back and forward buttons,
    # we need to listen to those events.
    activate: ->
        # Ensure we don't overwrite any previous `onpopstate` call.
        prev = window.onpopstate if window.onpopstate
        window.onpopstate = (event) =>
            prev(event) if prev
            @emit('route', window.location.pathname)
        window.onpopstate()
        return this

    # Route to a new view, given a path.
    # The new view is constructed and the previous view is removed.
    route: (path) ->
        # Find the matching view.
        View = @findView(path)

        # If no matching view, throw an error.
        if not View
            throw new Error("No matching view for path: #{path}")

        # Update the display of the URL.
        if path isnt window.location.pathname
            history.pushState({}, '', path)

        # Remove previous view instance.
        @view.remove() if @view

        # Create a new view instance.
        @view = new View({region: @region})

        return @view

    # Finds the view matching the path.
    findView: (docPath) ->
        for route in @routes
            [viewPath, View] = route
            if @matches(docPath, viewPath)
                return View

    # Determine if a given path matches this router.
    # Returns either false or array, where array is matches parameters.
    matches: (docPath, viewPath) ->
        if util.isString(viewPath)
            viewPath = new RegExp(
                '^' +
                viewPath.replace(/\{([\d\w\_\$]+)\}/g, '([^/]+)') +
                '$'
            )
        match = docPath.match(viewPath)
        return if match then match.slice(1) else false

    # When we click an internal link, use `route` instead
    bindLinks: ->
        return document.body.addEventListener('click', (e) =>
            el = util.closest(e.target, document.body, 'a')
            return if not el

            # Navigate to in-app URLs instead of new page
            if el.matches('[href^="/"]')
                e.preventDefault()
                @emit('route', el.pathname)
            # Do nothing on empty links
            else if el.matches('[href="#"]')
                e.preventDefault()
            # Open external URLs in new windows
            else if el.matches('[href*="//"]')
                el.target = '_blank'
        )

module.exports = Router
