define [
    'jquery'
    'backbone'
    'hbs/sections/public/contact'
], ($, Bb, t) ->

    class ContactView extends Bb.View

        el: $ '#page'
        template: t

        initialize: ->
            @render()

        render: ->
            document.title = 'Contact Sagefy.'
            @$el.attr 'id', 'contact'
                .html @template()
