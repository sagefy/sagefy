PageAdapter = require('./page')
ContactView = require('../views/contact')

class ContactAdapter extends PageAdapter
    url: '/contact'
    View: ContactView

module.exports = ContactAdapter
