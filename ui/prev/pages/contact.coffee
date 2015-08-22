View = require('../../modules/view')
aux = require('../../modules/auxiliaries')

class ContactPageView extends View

    constructor: ->
        super
        aux.setTitle('Contact')
        # TODO localize
        @render()

module.exports = ContactPageView
