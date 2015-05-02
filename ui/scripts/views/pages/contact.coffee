View = require('../../framework/view')
aux = require('../../modules/auxiliaries')

class ContactPageView extends View
    id: 'contact'
    className: 'col-8'
    template: require('../../templates/pages/contact')

    constructor: ->
        super
        aux.setTitle('Contact')
        # TODO localize
        @render()

module.exports = ContactPageView
