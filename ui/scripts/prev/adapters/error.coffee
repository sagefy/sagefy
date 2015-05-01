PageAdapter = require('./page')
View = require('../framework/view')
template = require('../templates/pages/error')
c = require('../modules/content').get

class ErrorAdapter extends PageAdapter
    title: c('error', 'code_404')

    render: ->
        super
        @view = new View({
            id: 'error'
            className: 'col-4'
            template: template
            region: @page
        })
        @view.render({
            code: 404
            message: c('error', 'code_404')
        })

    remove: ->
        @view.remove()
        super

module.exports = ErrorAdapter
