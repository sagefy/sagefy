$ = require('jquery')
Bb = require('backbone')
t = require('hbs/sections/public/terms')
mixins = require('modules/mixins')

module.exports = class TermsView extends Bb.View
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
