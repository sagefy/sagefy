


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
