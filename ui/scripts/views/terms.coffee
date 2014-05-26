$ = require('jquery')
Backbone = require('backbone')
template = require('../../templates/sections/public/terms')

class TermsView extends Backbone.View
    id: 'terms'
    className: 'max-width-10'
    template: template

    initialize: (options) ->
        @$region = options.$region
        @render()

    render: ->
        document.title = 'Sagefy Terms of Service.'
        @$el.html(@template())
        @$region.html(@$el)

module.exports = TermsView
