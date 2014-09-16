###
The app takes a series of adapters, and delegates URLs
to them when the URL changes.
###

Events = require('./events')

class App extends Events
    # The application instance takes a list of adapters
    constructor: (Adapters) ->
        super()
        for Adapter in Adapters
            @bindAdapter(Adapter)

    # Takes the URL of the adapter, and ensure that
    # when that URL is hit, the adapter is constructed and the
    # previous adapter is removed.
    bindAdapter: (Adapter) ->
        Adapter.navigate = @navigate

    # Remove unbindings so the adapter can be cleanly removed
    unbindAdapter: (Adapter) ->
        Adapter.navigate = null

    # Navigate the application to a specific URL
    navigate: ->

    # Removes the application
    remove: ->
        super()
        for Adapter in Adapters
            @unbindAdapter(Adapter)

module.exports = App
