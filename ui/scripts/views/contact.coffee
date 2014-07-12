$ = require('jquery')
PageView = require('./page')
template = require('../../templates/sections/public/contact')

class ContactView extends PageView
    id: 'contact'
    className: 'max-width-8'
    template: template
    title: 'Contact'

module.exports = ContactView
