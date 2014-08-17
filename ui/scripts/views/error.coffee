$ = require('jquery')
PageView = require('./page')
template = require('../../templates/sections/public/error')

class ErrorView extends PageView
    id: 'error'
    className: 'col-4'
    template: template
    title: 'Error'

    render: ->
        @templateData = {
            code: @options.code
            message: @options.message
        }
        super()

module.exports = ErrorView
