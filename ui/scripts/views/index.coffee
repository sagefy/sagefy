define([
    'jquery'
    'backbone'
    'hbs/sections/public/index'
], ($, Bb, t) ->

    class IndexView extends Bb.View

        el: $('.page')
        template: t

        initialize: ->
            @render()

        render: ->
            document.title = 'Sagefy - ' +
                'Adaptive, collaborative, and open learning platform.'
            @$el.addClass('max-width-8')
                .attr('id', 'index')
                .html(@template())


)
