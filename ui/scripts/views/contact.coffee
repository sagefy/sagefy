$ = require('jquery')
PageView = require('./page')
template = require('../templates/sections/public/contact')

class ContactView extends PageView
    id: 'contact'
    className: 'col-8'
    template: template
    title: 'Contact'

module.exports = ContactView
