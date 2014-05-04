define([
    'jquery'
    'backbone'
    'hbs/sections/public/contact'
    'modules/mixins'
], ($, Bb, t, mixins) ->

    class ContactView extends Bb.View

        el: $('.page')
        template: t

        initialize: ->
            @render()

        render: ->
            document.title = 'Contact Sagefy.'
            @$el.attr('id', 'contact')
                .html(@template())
            @updatePageWidth(8)

        updatePageWidth: mixins.updatePageWidth


)
