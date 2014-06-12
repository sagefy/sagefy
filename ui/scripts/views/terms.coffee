$ = require('jquery')
PageView = require('./page')
template = require('../../templates/sections/public/terms')

class TermsView extends PageView
    id: 'terms'
    className: 'max-width-10'
    template: template
    title: 'Sagefy Terms of Service.'

module.exports = TermsView
