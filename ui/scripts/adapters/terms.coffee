PageAdapter = require('./page')
View = require('../framework/view')
template = require('../templates/pages/terms')

class TermsAdapter extends PageAdapter
    url: '/terms'
    title: 'Terms of Service'

    constructor: ->
        @view = new View({
            id: 'terms'
            className: 'col-10'
            template: template
            region: @page
        })
        @view.render()
        super

    remove: ->
        @view.remove()
        super


module.exports = TermsAdapter
