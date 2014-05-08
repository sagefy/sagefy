Backbone = require('backbone')

module.exports = class ModelView extends Backbone.View
    initialize: ->
        if @beforeInitialize
            @beforeInitialize()

        @model.fetch()
        @listenTo(@model, 'sync', @render)

    render: =>
        @$el.html(@template(@model.toJSON()))
        @onRender()
