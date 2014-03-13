define([
    'jquery'
    'backbone'
    'hbs/sections/styleguide/index'
    'hbs/sections/styleguide/compiled'
], ($, Bb, t, t2) ->

    class StyleguideView extends Bb.View

        el: $('#page')
        template: t
        template2: t2

        events: {
            'click a[href="#"]': 'cancel'
            'click a[href*="//"]': 'openInNewWindow'
        }

        initialize: ->
            @render()

        render: ->
            document.title = 'Sagefy - Style Guide and Component Library.'

            @$el.addClass('max-width-10')
                .attr('id', 'styleguide')
                .html(@template())
                .append(@template2())

        cancel: ->
            false

        openInNewWindow: (e) ->
            $target = $(e.target).closest('a')
            $target[0].target = '_blank'


)
