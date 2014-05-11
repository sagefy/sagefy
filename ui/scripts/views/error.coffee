$ = require('jquery')
Bb = require('backbone')
t = require('../../templates/sections/public/error')
mixins = require('../modules/mixins')

module.exports = class ErrorView extends Bb.View
    el: $('.page')
    template: t

    initialize: ->
        @render()

    render: ->
        document.title = 'Error'
        @$el.attr('id', 'error')
            .html(@template({
                code: 404
                message: 'Not Found'
            }))
        @updatePageWidth(4)

    updatePageWidth: mixins.updatePageWidth
