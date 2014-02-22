define [
    'jquery'
    'backbone'
    'hbs/public/index'
], ($, Bb, t) ->

    class IndexView extends Bb.View

        el: $ 'body'

        initialize: ->
            @render()

        render: ->
            document.title = 'Sagefy - Adaptive, collaborative, and open learning platform.'
            @$el.addClass 'max-width-8'
                .attr 'id', 'index'
                .html t()
