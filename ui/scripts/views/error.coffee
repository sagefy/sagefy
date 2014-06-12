$ = require('jquery')
PageView = require('./page')
template = require('../../templates/sections/public/error')

class ErrorView extends PageView
    id: 'error'
    className: 'max-width-4'
    template: template
    title: 'Error'

    beforeRender: ->
        @templateData = {
            code: @options.code
            message: @options.message
        }

module.exports = ErrorView
