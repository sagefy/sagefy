define [
    'jquery'
    'backbone'
    'hbs/styleguide/index'
], ($, Bb, t) ->

    class StyleguideView extends Bb.View

        el: $ 'body'

        events:
            'click a[href="#"]': 'cancel'
            'click a[href*="//"]': 'openInNewWindow'

        initialize: ->
            @render()

        render: ->
            document.title = 'Sagefy - Style Guide and Component Library.'

            @$el.addClass 'max-width-10'
                .attr 'id', 'styleguide'
                .html t()

        cancel: ->
            false

        openInNewWindow: (e) ->
            $target = $(e.target).closest 'a'
            $target.target = "_blank"

