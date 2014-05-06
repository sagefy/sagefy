$ = require('jquery')
Backbone = require('backbone')
t = require('../../templates/sections/public/contact')
mixins = require('../modules/mixins')

module.exports = class ContactView extends Backbone.View
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
