$ = require('jquery')
Backbone = require('backbone')
template = require('../../templates/sections/public/contact')

class ContactView extends Backbone.View
    id: 'contact'
    className: 'max-width-8'
    template: template

    initialize: (options) ->
        @$region = options.$region
        @render()

    render: ->
        document.title = 'Contact Sagefy.'
        @$el.html(@template())
        @$region.html(@$el)

module.exports = ContactView
