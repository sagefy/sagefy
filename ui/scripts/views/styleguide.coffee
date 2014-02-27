define [
    'jquery'
    'backbone'
    'hbs/sections/styleguide/index'
], ($, Bb, t) ->

    class StyleguideView extends Bb.View

        el: $ '#page'
        template: t

        events:
            'click a[href="#"]': 'cancel'
            'click a[href*="//"]': 'openInNewWindow'

        initialize: ->
            @render()

        render: ->
            document.title = 'Sagefy - Style Guide and Component Library.'

            @$el.addClass 'max-width-10'
                .attr 'id', 'styleguide'
                .html @template()

        cancel: ->
            false

        openInNewWindow: (e) ->
            $target = $(e.target).closest 'a'
            $target[0].target = '_blank'

