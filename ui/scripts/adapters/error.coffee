PageAdapter = require('./page')
ErrorView = require('../views/error')

class ErrorAdapter extends PageAdapter
    url: /.*/
    View: ErrorView
    viewOptions: {
        code: 404
        message: 'Not Found'
    }

module.exports = ErrorAdapter
