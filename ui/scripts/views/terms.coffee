$ = require('jquery')
PageView = require('./page')
template = require('../../templates/sections/public/terms')

class TermsView extends PageView
    id: 'terms'
    className: 'col-10'
    template: template
    title: 'Terms of Service'

module.exports = TermsView
