View = require('../../modules/view')
aux = require('../../modules/auxiliaries')
c = require('../../modules/content').get

class ErrorPageView extends View
    id: 'error'
    className: 'col-4'
    template: require('./error.tmpl')

    constructor: ->
        super
        aux.setTitle(c('not_found'))
        @render({
            code: 404
            message: c('not_found')
        })

module.exports = ErrorPageView
