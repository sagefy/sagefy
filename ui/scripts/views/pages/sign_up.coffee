View = require('../../framework/view')
aux = require('../../modules/auxiliaries')

class SignUpPageView extends View
    constructor: ->
        super
        aux.setTitle('Sign Up')

module.exports = SignUpPageView
