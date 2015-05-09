View = require('../../modules/view')
aux = require('../../modules/auxiliaries')

class TermsPageView extends View
    id: 'terms'
    className: 'col-10'
    template: require('./terms.tmpl')

    constructor: ->
        super
        aux.setTitle('Terms of Service')
        # TODO localize
        @render()

module.exports = TermsPageView
