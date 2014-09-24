PageAdapter = require('./page')
IndexView = require('../views/index')

class IndexAdapter extends PageAdapter
    url: /^\/?$/
    View: IndexView

module.exports = IndexAdapter
