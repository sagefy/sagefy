View = require('../../framework/view')
aux = require('../../modules/auxiliaries')

class LogOutPageView extends View
    constructor: ->
        super
        aux.setTitle('Logging Out...')

module.exports = LogOutPageView
