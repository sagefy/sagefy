View = require('../../modules/view')
aux = require('../../modules/auxiliaries')

class ContactPageView extends View
    id: 'contact'
    className: 'col-8'
    template: require('./contact.tmpl')

    constructor: ->
        super
        aux.setTitle('Contact')
        # TODO localize
        @render()

module.exports = ContactPageView
