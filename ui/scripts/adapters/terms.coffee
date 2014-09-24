PageAdapter = require('./page')
TermsView = require('../views/terms')

class TermsAdapter extends PageAdapter
    url: '/terms'
    View: TermsView

module.exports = TermsAdapter
