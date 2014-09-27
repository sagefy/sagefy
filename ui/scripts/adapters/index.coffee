PageAdapter = require('./page')
View = require('../framework/view')
mixins = require('../modules/mixins')
template = require('../templates/pages/index')

class IndexAdapter extends PageAdapter
    url: /^\/?$/
    title: 'Adaptive, Collaborative, and Open Learning Platform'

    constructor: ->
        super
        @view = new View({
            id: 'index'
            className: 'col-8'
            template: template
            region: @page
        })
        @view.render({
            isLoggedIn: @isLoggedIn()
        })

    remove: ->
        @view.remove()
        super

module.exports = IndexAdapter
