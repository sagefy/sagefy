PageAdapter = require('./page')
View = require('../framework/view')
template = require('../templates/pages/error')
g = require('../modules/content').get

class ErrorAdapter extends PageAdapter
    url: /.*/
    title: g('error', 'code_404')

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
            message: g('error', 'code_404')
        })

    remove: ->
        @view.remove()
        super

module.exports = ErrorAdapter
