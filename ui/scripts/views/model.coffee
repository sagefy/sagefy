Backbone = require('backbone')

class ModelView extends Backbone.View
    initialize: (options = {}) ->
        @$region = options.$region || $({})

        if options.model
            @model = options.model

        if @beforeInitialize
            @beforeInitialize()

        @model.fetch()
        @listenTo(@model, 'sync', @render)

    render: =>
        @$el.html(@template(@model.toJSON()))
        @$region.html(@$el)
        @onRender()


module.exports = ModelView
