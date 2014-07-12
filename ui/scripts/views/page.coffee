$ = require('jquery')
Backbone = require('backbone')

class PageView extends Backbone.View
    initialize: (options) ->
        @options = options
        @$region = @options.$region
        if @model
            @listenTo(@model, 'sync', @render)
        else
            @render()

    render: =>
        if @beforeRender
            @beforeRender()

        document.title = (@title || '') + ' -- Sagefy'
        templateData = @model?.toJSON() || @templateData || null

        @$el.html(@template(templateData))
        @$region.html(@$el)

module.exports = PageView
