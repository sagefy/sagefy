$ = require('jquery')
Backbone = require('backbone')
template = require('../../templates/sections/public/error')

class ErrorView extends Backbone.View
    id: 'error'
    className: 'max-width-4'
    template: template

    initialize: (options) ->
        @$region = options.$region
        @code = options.code
        @message = options.message
        @render()

    render: ->
        document.title = 'Error'
        @$el.html(@template({
            code: @code
            message: @message
        }))
        @$region.html(@$el)

module.exports = ErrorView
