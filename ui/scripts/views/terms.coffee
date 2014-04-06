define([
    'jquery'
    'backbone'
    'hbs/sections/public/terms'
], ($, Bb, t) ->

    class TermsView extends Bb.View

        el: $('.page')
        template: t

        initialize: ->
            @render()

        render: ->
            document.title = 'Sagefy Terms of Service.'
            @$el.addClass('max-width-12')
                .attr('id', 'terms')
                .html(@template())


)
