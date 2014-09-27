PageAdapter = require('./page')
UserModel = require('../models/user')
# SignupView = require('../views/signup')

class SignupAdapter extends PageAdapter
    url: '/signup'
    title: 'Create Account'

    constructor: ->
        super
        @model = new UserModel()
        # @view = new SignupView()

    remove: ->
        @view.remove()
        @model.remove()
        super

module.exports = SignupAdapter
