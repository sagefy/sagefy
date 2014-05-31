Backbone = require('backbone')
_ = require('underscore')

class BaseRouter extends Backbone.Router
    route: (route, name, callback) ->
        prevCallback = callback || @[name]

        callback = =>
            if _.isFunction(@beforeRoute)
                @beforeRoute()
            prevCallback.call(this, arguments)

        super(route, name, callback)

    beforeRoute: ->
        if @controller
            @controller.close()

module.exports = BaseRouter
