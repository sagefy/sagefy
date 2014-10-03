PageAdapter = require('./page')
View = require('../framework/view')
template = require('../templates/pages/error')

class ErrorAdapter extends PageAdapter
    url: /.*/
    title: 'Not Found'

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
            message: 'Not Found'
        })

    remove: ->
        @view.remove()
        super

module.exports = ErrorAdapter
