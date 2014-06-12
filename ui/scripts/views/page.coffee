$ = require('jquery')
Backbone = require('backbone')

class PageView extends Backbone.View
    initialize: (options) ->
        @options = options
        @$region = @options.$region
        @render()

    render: ->
        if @beforeRender
            @beforeRender()

        document.title = @title || ''
        templateData = @model?.toJSON() || @templateData || null

        @$el.html(@template(templateData))
        @$region.html(@$el)

module.exports = PageView
