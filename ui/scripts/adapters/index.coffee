PageAdapter = require('./page')
View = require('../framework/view')
mixins = require('../modules/mixins')
template = require('../templates/pages/index')

class IndexAdapter extends PageAdapter
    url: /^\/?$/
    title: 'Adaptive, Collaborative, and Open Learning Platform'
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

    isLoggedIn: mixins.isLoggedIn

module.exports = IndexAdapter
