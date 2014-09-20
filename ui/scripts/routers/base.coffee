Backbone = require('backbone')
_ = require('underscore')

# Enables some route memory management
class BaseRouter extends Backbone.Router
    # Enable a `beforeRoute` function
    route: (route, name, callback) ->
        # Store the route function
        prevCallback = callback || @[name]

        # Enable the `beforeRoute`
        callback = =>
            if _.isFunction(@beforeRoute)
                @beforeRoute()
            prevCallback.call(this, arguments)

        # Call the Backbone router with updated callback
        super

    # Closes any existing routers, and by extension,
    # Any children the controller contains
    beforeRoute: ->
        if @controller
            @controller.close()

module.exports = BaseRouter
