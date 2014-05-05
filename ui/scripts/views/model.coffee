define([
    'backbone'
], (Backbone) ->

    class ModelView extends Backbone.View

        initialize: ->
            if @beforeInitialize
                @beforeInitialize()

            @model.fetch()
            @model.on('sync', @render)

        render: =>
            @$el.html(@template(@model.toJSON()))
            @onRender()

)
