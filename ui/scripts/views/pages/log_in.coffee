View = require('../../framework/view')
aux = require('../../modules/auxiliaries')

class LogInPageView extends View
    constructor: ->
        super
        aux.setTitle('Log In')

module.exports = LogInPageView
