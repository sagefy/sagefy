define([
    'jquery'
    'backbone'
    'hbs/sections/styleguide/index'
    'hbs/sections/styleguide/compiled'
    'modules/mixins'
], ($, Bb, t, t2, mixins) ->

    class StyleguideView extends Bb.View

        el: $('.page')
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

            @$el.attr('id', 'styleguide')
                .html(@template())
                .append(@template2())

            @updatePageWidth(10)

        cancel: ->
            false

        openInNewWindow: (e) ->
            $target = $(e.target).closest('a')
            $target[0].target = '_blank'

        updatePageWidth: mixins.updatePageWidth


)
