PageAdapter = require('./page')
UserModel = require('../models/user')
# LoginView = require('../views/login')

class LoginAdapter extends PageAdapter
    url: '/login'
    title: 'Login'

    constructor: ->
        super
        @model = new UserModel()
        # @view = new LoginView()

    remove: ->
        # @view.remove()
        @model.remove()
        super

module.exports = LoginAdapter
