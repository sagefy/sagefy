Backbone = require('backbone')
_ = require('underscore')

class Controller extends Backbone.Events
    constructor: (options) ->
        if @initialize
            @initialize(options)

    close: ->
        @stopListening()
        @off()

module.exports = Controller
