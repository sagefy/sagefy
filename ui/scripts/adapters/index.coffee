PageAdapter = require('./page')
View = require('../framework/view')
aux = require('../modules/auxiliaries')
template = require('../templates/pages/index')

class IndexAdapter extends PageAdapter
    url: /^\/?$/
    title: 'Adaptive, Collaborative, and Open Learning Platform'
    # TODO move copy to content directory

    render: ->
        return if @requireLogOut()
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

    isLoggedIn: aux.isLoggedIn

module.exports = IndexAdapter
