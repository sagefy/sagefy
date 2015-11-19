broker = require('../modules/broker')
actions = require('../modules/actions')

module.exports = broker.add({
    # When we click an internal link, use `route` instead
    'click a[href^="/"]': (e, el) ->
        e.preventDefault()
        window.scrollTo(0, 0)
        actions.route(el.pathname + el.search)

    # Do nothing on empty links
    'click a[href="#"]': (e, el) ->
        e.preventDefault()

    # Open external URLs in new windows
    'click a[href*="//"]': (e, el) ->
        el.target = '_blank'
})
