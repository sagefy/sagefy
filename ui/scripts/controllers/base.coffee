Backbone = require('backbone')
_ = require('underscore')

class Controller extends Backbone.Events
    constructor: (options) ->
        if _.isFunction(@initialize)
            @initialize(options)

    close: ->
        if _.isFunction(@beforeClose)
            @beforeClose()

        # @stopListening()
        # @off()

module.exports = Controller
