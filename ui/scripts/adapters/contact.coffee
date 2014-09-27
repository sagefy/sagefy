PageAdapter = require('./page')
View = require('../framework/view')
template = require('../templates/pages/contact')

class ContactAdapter extends PageAdapter
    url: '/contact'
    title: 'Contact'

    constructor: ->
        super
        @view = new View({
            id: 'contact'
            className: 'col-8'
            template: template
            region: @page
        })
        @view.render()

    remove: ->
        @view.remove()
        super

module.exports = ContactAdapter
