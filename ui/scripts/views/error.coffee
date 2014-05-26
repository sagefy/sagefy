$ = require('jquery')
Backbone = require('backbone')
template = require('../../templates/sections/public/error')

class ErrorView extends Backbone.View
    id: 'error'
    className: 'max-width-4'
    template: template

    initialize: (options) ->
        @$region = options.$region
        @render()

    render: ->
        document.title = 'Error'
        @$el.html(@template({
            code: 404
            message: 'Not Found'
        }))
        @$region.html(@$el)

module.exports = ErrorView
