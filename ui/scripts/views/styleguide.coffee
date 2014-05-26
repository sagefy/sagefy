$ = require('jquery')
Backbone = require('backbone')
t = require('../../templates/sections/styleguide/index')
t2 = require('../../templates/sections/styleguide/compiled')
mixins = require('../modules/mixins')

class StyleguideView extends Backbone.View
    id: 'styleguide'
    className: 'max-width-10'
    template: t
    template2: t2

    events: {
        'click a[href="#"]': 'cancel'
        'click a[href*="//"]': 'openInNewWindow'
    }

    initialize: (options) ->
        @$region = options.$region
        @render()

    render: ->
        document.title = 'Sagefy - Style Guide and Component Library.'
        @$el.html(@template())
            .append(@template2())
        @$region.html(@$el)

    cancel: ->
        return false

    openInNewWindow: (e) ->
        $target = $(e.target).closest('a')
        $target[0].target = '_blank'

module.exports = StyleguideView
