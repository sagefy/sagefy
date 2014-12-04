PageAdapter = require('./page')
View = require('../framework/view')
utilities = require('../modules/utilities')
template = require('../templates/pages/index')

class IndexAdapter extends PageAdapter
    url: /^\/?$/
    title: 'Adaptive, Collaborative, and Open Learning Platform'
    # TODO: move copy to content directory
    requireLogout: true

    render: ->
        super
        @view = new View({
            id: 'index'
            className: 'col-8'
            template: template
            region: @page
        })
        @view.render()

    remove: ->
        @view.remove()
        super

    isLoggedIn: utilities.isLoggedIn

module.exports = IndexAdapter
