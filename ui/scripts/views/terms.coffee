define([
    'jquery'
    'backbone'
    'hbs/sections/public/terms'
    'modules/mixins'
], ($, Bb, t, mixins) ->

    class TermsView extends Bb.View

        el: $('.page')
        template: t

        initialize: ->
            @render()

        render: ->
            document.title = 'Sagefy Terms of Service.'
            @$el.attr('id', 'terms')
                .html(@template())
            @updatePageWidth(10)

        updatePageWidth: mixins.updatePageWidth

)
