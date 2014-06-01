Backbone = require('backbone')
_ = require('underscore')

class Controller
    constructor: (options) ->
        # http://stackoverflow.com/a/11068223/1509526
        _.extend(this, Backbone.Events)

        if _.isFunction(@initialize)
            @initialize(options)

    close: ->
        @stopListening()
        @off()

module.exports = Controller
